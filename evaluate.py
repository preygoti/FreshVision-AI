"""
Model Evaluation, Metric Computation, and Visualization Generator
Evaluates the trained model strictly on the untouched test split (data/dataset.csv).
Generates:
- Confusion Matrix Heatmap (static/results/confusion_matrix.png)
- Training vs Validation Learning Curves (static/results/training_curves.png)
- Per-class Precision, Recall, F1 metrics (models/class_metrics.json)
- Formatted Classification Report (models/classification_report.txt)
"""

import os
import json
import csv
import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset
from PIL import Image
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from model import FruitFreshnessClassifier, PREPROCESS_TRANSFORMS, CLASSES


class TestDatasetFromCSV(Dataset):
    def __init__(self, csv_path, split="test", transform=None):
        self.records = []
        self.transform = transform
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["split"] == split:
                    self.records.append((row["image_path"], CLASSES.index(row["label"])))

    def __len__(self):
        return len(self.records)

    def __getitem__(self, idx):
        path, label = self.records[idx]
        with Image.open(path) as img:
            img_rgb = img.convert("RGB")
        if self.transform:
            img_rgb = self.transform(img_rgb)
        return img_rgb, label


def plot_confusion_matrix(cm, accuracy, output_paths):
    plt.figure(figsize=(9, 7.5), dpi=200)
    sns.set_theme(style="white")
    
    ax = sns.heatmap(
        cm, annot=True, fmt='d', cmap='Blues',
        xticklabels=CLASSES, yticklabels=CLASSES,
        cbar_kws={'label': 'Number of Images'}
    )
    plt.title(
        f"Test Confusion Matrix\nAccuracy: {accuracy * 100:.2f}% | Real Fruit Dataset (MobileNetV2)",
        fontsize=13, pad=16, fontweight='bold', color='#0f172a'
    )
    plt.xlabel('Predicted Class', fontsize=11, fontweight='bold', color='#1e293b')
    plt.ylabel('Ground Truth Class', fontsize=11, fontweight='bold', color='#1e293b')
    plt.xticks(rotation=25, ha='right', fontsize=9.5)
    plt.yticks(rotation=0, fontsize=9.5)
    plt.tight_layout()
    
    for path in output_paths:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"[+] Saved confusion matrix to: {output_paths}")


def plot_training_curves(history, output_paths):
    epochs = history.get("epoch", [])
    train_loss = history.get("train_loss", [])
    val_loss = history.get("val_loss", [])
    train_acc = history.get("train_acc", [])
    val_acc = history.get("val_acc", [])

    if not epochs or len(epochs) == 0:
        print("[!] No training history available to plot curves.")
        return

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=200)

    # Loss plot
    ax1.plot(epochs, train_loss, 'o-', color='#e11d48', label='Training Loss', linewidth=2, markersize=6)
    ax1.plot(epochs, val_loss, 's--', color='#0284c7', label='Validation Loss', linewidth=2, markersize=6)
    ax1.set_title('Cross-Entropy Loss vs. Epochs', fontsize=12, fontweight='bold', color='#0f172a')
    ax1.set_xlabel('Epoch', fontsize=10.5, fontweight='bold')
    ax1.set_ylabel('Loss', fontsize=10.5, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper right', frameon=True)

    # Accuracy plot
    ax2.plot(epochs, train_acc, 'o-', color='#059669', label='Training Accuracy', linewidth=2, markersize=6)
    ax2.plot(epochs, val_acc, 's--', color='#ea580c', label='Validation Accuracy', linewidth=2, markersize=6)
    ax2.set_title('Model Accuracy vs. Epochs', fontsize=12, fontweight='bold', color='#0f172a')
    ax2.set_xlabel('Epoch', fontsize=10.5, fontweight='bold')
    ax2.set_ylabel('Accuracy (%)', fontsize=10.5, fontweight='bold')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='lower right', frameon=True)

    plt.suptitle('FreshVision AI — Real Training Convergence Curves (MobileNetV2)', fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout()

    for path in output_paths:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"[+] Saved training curves to: {output_paths}")


def evaluate_model(
    model_path="models/best_model.pt",
    csv_path="data/dataset.csv",
    history_path="models/training_history.json",
    batch_size=32
):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Evaluating model on device: {device}")

    if not os.path.exists(model_path):
        # Fallback to fruit_classifier.pt if best_model.pt not found
        fallback = "models/fruit_classifier.pt"
        if os.path.exists(fallback):
            model_path = fallback
        else:
            raise FileNotFoundError(f"Model checkpoint not found at {model_path} or {fallback}")

    print(f"[*] Loading checkpoint: {model_path}")
    model = FruitFreshnessClassifier(num_classes=6, pretrained=False).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    test_dataset = TestDatasetFromCSV(csv_path, split="test", transform=PREPROCESS_TRANSFORMS)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    print(f"[*] Test dataset size: {len(test_dataset)} samples")

    y_true = []
    y_pred = []

    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            outputs = model(images)
            _, preds = torch.max(outputs, 1)
            y_true.extend(labels.cpu().numpy().tolist())
            y_pred.extend(preds.cpu().numpy().tolist())

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    # Compute metrics
    acc = float(accuracy_score(y_true, y_pred))
    prec_macro = float(precision_score(y_true, y_pred, average="macro", zero_division=0))
    rec_macro = float(recall_score(y_true, y_pred, average="macro", zero_division=0))
    f1_macro = float(f1_score(y_true, y_pred, average="macro", zero_division=0))

    prec_weighted = float(precision_score(y_true, y_pred, average="weighted", zero_division=0))
    rec_weighted = float(recall_score(y_true, y_pred, average="weighted", zero_division=0))
    f1_weighted = float(f1_score(y_true, y_pred, average="weighted", zero_division=0))

    cm = confusion_matrix(y_true, y_pred, labels=list(range(6)))
    report_dict = classification_report(y_true, y_pred, target_names=CLASSES, output_dict=True, zero_division=0)
    report_text = classification_report(y_true, y_pred, target_names=CLASSES, zero_division=0)

    print("\n" + "="*60)
    print("TEST EVALUATION RESULTS (ACTUAL)")
    print("="*60)
    print(f"Test Accuracy:          {acc * 100:.2f}%")
    print(f"Macro Precision:        {prec_macro * 100:.2f}%")
    print(f"Macro Recall:           {rec_macro * 100:.2f}%")
    print(f"Macro F1-Score:         {f1_macro * 100:.2f}%")
    print(f"Weighted F1-Score:      {f1_weighted * 100:.2f}%")
    print("\nDetailed Classification Report:")
    print(report_text)
    print("="*60)

    # Save classification report text
    os.makedirs("models", exist_ok=True)
    with open("models/classification_report.txt", "w", encoding="utf-8") as f:
        f.write(report_text)
        f.write(f"\nOverall Test Accuracy: {acc * 100:.2f}%\n")
        f.write(f"Macro F1-Score:        {f1_macro * 100:.2f}%\n")
        f.write(f"Weighted F1-Score:     {f1_weighted * 100:.2f}%\n")

    # Format per-class metrics dictionary
    per_class = {}
    for i, cls in enumerate(CLASSES):
        cls_data = report_dict.get(cls, {})
        per_class[cls] = {
            "precision": round(float(cls_data.get("precision", 0)) * 100, 2),
            "recall": round(float(cls_data.get("recall", 0)) * 100, 2),
            "f1_score": round(float(cls_data.get("f1-score", 0)) * 100, 2),
            "support": int(cls_data.get("support", 0))
        }

    metrics_payload = {
        "status": "success",
        "dataset": "Real Fruit Freshness Dataset (Kaggle)",
        "model_architecture": "MobileNetV2 (Transfer Learning)",
        "num_classes": 6,
        "classes": CLASSES,
        "test_samples": len(test_dataset),
        "overall_accuracy_pct": round(acc * 100, 2),
        "macro_precision_pct": round(prec_macro * 100, 2),
        "macro_recall_pct": round(rec_macro * 100, 2),
        "macro_f1_pct": round(f1_macro * 100, 2),
        "weighted_f1_pct": round(f1_weighted * 100, 2),
        "per_class_metrics": per_class,
        "confusion_matrix": cm.tolist()
    }

    with open("models/class_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, indent=2)
    print("[+] Saved metrics payload to models/class_metrics.json")

    # Generate Confusion Matrix plot
    cm_paths = [
        "static/results/confusion_matrix.png",
        "static/charts/confusion_matrix.png"
    ]
    plot_confusion_matrix(cm, acc, cm_paths)

    # Generate Learning Curves if history exists
    if os.path.exists(history_path):
        with open(history_path, "r", encoding="utf-8") as f:
            history = json.load(f)
        curve_paths = [
            "static/results/training_curves.png",
            "static/charts/training_validation_curves.png"
        ]
        plot_training_curves(history, curve_paths)

    return metrics_payload


if __name__ == "__main__":
    evaluate_model()
