"""
Real Benchmark Image Loader for FreshVision AI
Populates static/samples/ using genuine test set images from the real dataset.
Group 7 College Capstone Project
"""

import os
import csv
from pathlib import Path
from PIL import Image

CLASS_TO_PRESET = {
    "Fresh Apple": "freshapples.jpg",
    "Rotten Apple": "rottenapples.jpg",
    "Fresh Banana": "freshbanana.jpg",
    "Rotten Banana": "rottenbanana.jpg",
    "Fresh Orange": "freshoranges.jpg",
    "Rotten Orange": "rottenoranges.jpg",
}

def generate_all_samples(output_dir="static/samples", csv_path="data/dataset.csv"):
    os.makedirs(output_dir, exist_ok=True)
    saved_paths = {}

    # Extract 1 representative real image per class from the test split
    if os.path.exists(csv_path):
        found = {}
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                lbl = row["label"]
                split = row["split"]
                if split == "test" and lbl in CLASS_TO_PRESET and lbl not in found:
                    found[lbl] = row["image_path"]
                if len(found) == len(CLASS_TO_PRESET):
                    break

        for lbl, filename in CLASS_TO_PRESET.items():
            if lbl in found and os.path.exists(found[lbl]):
                out_path = os.path.join(output_dir, filename)
                with Image.open(found[lbl]) as img:
                    img.convert("RGB").save(out_path, format="JPEG", quality=95)
                saved_paths[filename] = out_path
                print(f"[+] Loaded real test sample for {lbl} -> {out_path}")
            else:
                print(f"[!] Warning: Test sample for {lbl} not found in CSV.")
    else:
        print(f"[!] CSV not found at {csv_path}, cannot copy real sample images.")

    return saved_paths

if __name__ == "__main__":
    generate_all_samples()
