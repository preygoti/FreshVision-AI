import os
import csv
from pathlib import Path
from collections import defaultdict
import random

DATASET_ROOT = Path(os.environ.get("DATASET_ROOT", r"C:\Users\ventura\Downloads\archive\dataset"))
OUTPUT_CSV = Path(r"C:\Users\ventura\.gemini\antigravity\scratch\fruit-freshness-detection\data\dataset.csv")

CLASS_MAPPING = {
    "freshapples": "Fresh Apple",
    "freshbanana": "Fresh Banana",
    "freshoranges": "Fresh Orange",
    "rottenapples": "Rotten Apple",
    "rottenbanana": "Rotten Banana",
    "rottenoranges": "Rotten Orange"
}

OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

print("="*60)
print("GENERATING REAL dataset.csv")
print(f"Dataset source root: {DATASET_ROOT}")
print("="*60)

train_dir = DATASET_ROOT / "train"
test_dir = DATASET_ROOT / "test"

if not train_dir.exists() or not test_dir.exists():
    raise FileNotFoundError(f"Missing train or test directory in {DATASET_ROOT}")

random.seed(42)

records = []
split_stats = defaultdict(lambda: defaultdict(int))

# Process train folder -> split 80% train / 20% validation (stratified by class)
for folder_name, label in CLASS_MAPPING.items():
    cls_folder = train_dir / folder_name
    files = sorted(list(cls_folder.glob("*.png")))
    # Shuffle with fixed seed for reproducibility
    shuffled_files = files.copy()
    random.shuffle(shuffled_files)
    
    n_total = len(shuffled_files)
    n_train = int(round(0.80 * n_total))
    
    train_files = shuffled_files[:n_train]
    val_files = shuffled_files[n_train:]
    
    for f in train_files:
        norm_path = f.as_posix()
        records.append({
            "image_path": norm_path,
            "label": label,
            "split": "train"
        })
        split_stats["train"][label] += 1
        
    for f in val_files:
        norm_path = f.as_posix()
        records.append({
            "image_path": norm_path,
            "label": label,
            "split": "val"
        })
        split_stats["val"][label] += 1

# Process test folder -> 100% test (final untouched test set)
for folder_name, label in CLASS_MAPPING.items():
    cls_folder = test_dir / folder_name
    files = sorted(list(cls_folder.glob("*.png")))
    for f in files:
        norm_path = f.as_posix()
        records.append({
            "image_path": norm_path,
            "label": label,
            "split": "test"
        })
        split_stats["test"][label] += 1

# Write CSV
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["image_path", "label", "split"])
    writer.writeheader()
    writer.writerows(records)

print(f"\n[+] Wrote {len(records)} records to {OUTPUT_CSV}")

# Print breakdown
print("\n--- SPLIT DISTRIBUTION BY CLASS ---")
all_labels = list(CLASS_MAPPING.values())
header = f"{'Label':16s} | {'Train (80%)':11s} | {'Val (20%)':9s} | {'Test (Kaggle)':13s} | {'Total':6s}"
print(header)
print("-" * len(header))

grand_train = sum(split_stats["train"].values())
grand_val = sum(split_stats["val"].values())
grand_test = sum(split_stats["test"].values())

for lbl in all_labels:
    tr = split_stats["train"][lbl]
    va = split_stats["val"][lbl]
    te = split_stats["test"][lbl]
    tot = tr + va + te
    print(f"{lbl:16s} | {tr:11d} | {va:9d} | {te:13d} | {tot:6d}")

print("-" * len(header))
print(f"{'TOTAL':16s} | {grand_train:11d} | {grand_val:9d} | {grand_test:13d} | {grand_train + grand_val + grand_test:6d}")

# VALIDATION STEP
print("\n" + "="*60)
print("CSV VALIDATION")
print("="*60)

seen_paths = set()
missing_paths = 0
duplicate_paths = 0
invalid_labels = 0
empty_labels = 0
valid_paths = 0

valid_labels_set = set(CLASS_MAPPING.values())

for row in records:
    path_str = row["image_path"]
    lbl = row["label"]
    
    if not lbl or lbl.strip() == "":
        empty_labels += 1
    elif lbl not in valid_labels_set:
        invalid_labels += 1
        
    if path_str in seen_paths:
        duplicate_paths += 1
    seen_paths.add(path_str)
    
    # Check filesystem existence
    if os.path.exists(path_str):
        valid_paths += 1
    else:
        missing_paths += 1

print(f"CSV rows:           {len(records)}")
print(f"Valid image paths:  {valid_paths}")
print(f"Missing image paths:{missing_paths}")
print(f"Duplicate paths:    {duplicate_paths}")
print(f"Empty labels:       {empty_labels}")
print(f"Invalid labels:     {invalid_labels}")
print("="*60)
