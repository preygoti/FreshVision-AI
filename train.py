"""
PyTorch Real Image Training Pipeline for Fruit Freshness Classification
Uses MobileNetV2 Transfer Learning with frozen feature backbone.
Trains strictly on the real dataset via data/dataset.csv.
Group 7 College Capstone Project
"""

import os
import sys
import time
import json
import csv
import argparse
from pathlib import Path
from PIL import Image

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms

from model import FruitFreshnessClassifier, PREPROCESS_TRANSFORMS, CLASSES
from evaluate import evaluate_model

# Data augmentation for training
TRAIN_TRANSFORMS = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(degrees=15),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


class FruitCSVDataset(Dataset):
    """
    Loads real fruit images directly from paths referenced in dataset.csv.
    """
    def __init__(self, csv_path, split="train", transform=None):
        self.records = []
        self.transform = transform
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["split"] == split:
                    self.records.append((row["image_path"], CLASSES.index(row["label"])))

        if len(self.records) == 0:
            raise ValueError(f"No records found in {csv_path} with split='{split}'")

    def __len__(self):
        return len(self.records)

    def __getitem__(self, idx):
        path, label = self.records[idx]
        with Image.open(path) as img:
            img_rgb = img.convert("RGB")
        if self.transform:
            img_rgb = self.transform(img_rgb)
        return img_rgb, label


def train_model(
    csv_path="data/dataset.csv",
    epochs=3,
    batch_size=64,
    lr=0.001,
    models_dir="models"
):
    torch.manual_seed(42)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("="*60)
    print("STARTING REAL MODEL TRAINING")
    print(f"Device:               {device}")
    print(f"Dataset CSV:          {csv_path}")
    print(f"Epochs:               {epochs}")
    print(f"Batch Size:           {batch_size}")
    print(f"Learning Rate:        {lr}")
    print("="*60)

    os.makedirs(models_dir, exist_ok=True)
    best_model_path = os.path.join(models_dir, "best_model.pt")
    final_model_path = os.path.join(models_dir, "final_model.pt")
    app_model_path = os.path.join(models_dir, "fruit_classifier.pt")
    history_path = os.path.join(models_dir, "training_history.json")

    # Load datasets
    train_dataset = FruitCSVDataset(csv_path, split="train", transform=TRAIN_TRANSFORMS)
    val_dataset = FruitCSVDataset(csv_path, split="val", transform=PREPROCESS_TRANSFORMS)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    print(f"[+] Loaded {len(train_dataset)} training images ({len(train_loader)} batches)")
    print(f"[+] Loaded {len(val_dataset)} validation images ({len(val_loader)} batches)")

    # Model: Transfer learning with MobileNetV2
    print("[*] Initializing MobileNetV2 with ImageNet pretrained backbone...")
    model = FruitFreshnessClassifier(num_classes=6, pretrained=True).to(device)

    # Freeze feature extractor
    for param in model.features.parameters():
        param.requires_grad = False

    # Trainable parameters are strictly in the custom classifier head
    trainable_params = [p for p in model.parameters() if p.requires_grad]
    print(f"[+] Frozen feature extractor. Training {sum(p.numel() for p in trainable_params)} classifier parameters.")

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(trainable_params, lr=lr, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=2, gamma=0.5)

    history = {
        "epoch": [],
        "train_loss": [],
        "train_acc": [],
        "val_loss": [],
        "val_acc": []
    }

    best_val_acc = 0.0
    start_total_time = time.time()

    for epoch in range(1, epochs + 1):
        epoch_start = time.time()
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        print(f"\n--- Epoch {epoch}/{epochs} ---")
        for batch_idx, (images, labels) in enumerate(train_loader, 1):
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            correct += torch.sum(preds == labels.data).item()
            total += labels.size(0)

            if batch_idx % 25 == 0 or batch_idx == len(train_loader):
                batch_acc = (correct / total) * 100
                batch_loss = running_loss / total
                print(f"  Batch [{batch_idx:03d}/{len(train_loader):03d}] | Loss: {batch_loss:.4f} | Acc: {batch_acc:.2f}%")

        scheduler.step()
        epoch_train_loss = running_loss / len(train_dataset)
        epoch_train_acc = (correct / len(train_dataset)) * 100

        # Validation pass
        model.eval()
        val_running_loss = 0.0
        val_correct = 0
        val_total = 0

        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)

                val_running_loss += loss.item() * images.size(0)
                _, preds = torch.max(outputs, 1)
                val_correct += torch.sum(preds == labels.data).item()
                val_total += labels.size(0)

        epoch_val_loss = val_running_loss / len(val_dataset)
        epoch_val_acc = (val_correct / len(val_dataset)) * 100
        epoch_duration = time.time() - epoch_start

        # Record actual history
        history["epoch"].append(epoch)
        history["train_loss"].append(round(epoch_train_loss, 4))
        history["train_acc"].append(round(epoch_train_acc, 2))
        history["val_loss"].append(round(epoch_val_loss, 4))
        history["val_acc"].append(round(epoch_val_acc, 2))

        print(
            f"Epoch {epoch} Completed ({epoch_duration:.1f}s) | "
            f"Train Loss: {epoch_train_loss:.4f} | Train Acc: {epoch_train_acc:.2f}% | "
            f"Val Loss: {epoch_val_loss:.4f} | Val Acc: {epoch_val_acc:.2f}%"
        )

        # Checkpoint best model
        if epoch_val_acc > best_val_acc:
            best_val_acc = epoch_val_acc
            torch.save(model.state_dict(), best_model_path)
            torch.save(model.state_dict(), app_model_path)
            print(f"  [*] New best validation accuracy: {best_val_acc:.2f}%. Saved to {best_model_path}")

    # Save final model
    torch.save(model.state_dict(), final_model_path)
    print(f"\n[+] Saved final model to: {final_model_path}")

    # Save training history JSON
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)
    print(f"[+] Saved training history to: {history_path}")

    total_duration = time.time() - start_total_time
    print(f"\n[+] Total training time: {total_duration/60:.2f} minutes")
    print("="*60)

    # Run evaluation strictly on final test set
    print("\n[*] Launching evaluation on untouched test set...")
    evaluate_model(
        model_path=best_model_path,
        csv_path=csv_path,
        history_path=history_path
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Fruit Freshness Classifier on Real Dataset")
    parser.add_argument("--csv_path", type=str, default="data/dataset.csv")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument("--lr", type=float, default=0.001)
    args = parser.parse_args()

    train_model(
        csv_path=args.csv_path,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr
    )
