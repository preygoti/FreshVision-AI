import os
import sys
from pathlib import Path
from collections import defaultdict
from PIL import Image

archive_path = Path(r"C:\Users\ventura\Downloads\archive")

if not archive_path.exists():
    print(f"ERROR: Dataset path does not exist: {archive_path}")
    sys.exit(1)

print("="*60)
print(f"INSPECTING ARCHIVE AT: {archive_path}")
print("="*60)

# List top level
for item in archive_path.iterdir():
    print(f"Top-level: {item.name} [{'DIR' if item.is_dir() else 'FILE'}]")

# Recursively search for image files and CSVs
image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff"}
images_found = []
csvs_found = []
all_files = []

for root, dirs, files in os.walk(archive_path):
    for f in files:
        fp = Path(root) / f
        all_files.append(fp)
        suffix = fp.suffix.lower()
        if suffix in image_extensions:
            images_found.append(fp)
        elif suffix == ".csv":
            csvs_found.append(fp)

print(f"\nTotal files found in archive: {len(all_files)}")
print(f"Total image files found: {len(images_found)}")
print(f"Total CSV files found: {len(csvs_found)}")
for csv in csvs_found:
    print(f"  CSV: {csv} ({csv.stat().st_size} bytes)")

# Analyze folder structure / splits / classes
folders_with_images = defaultdict(int)
for img in images_found:
    parent = img.parent
    folders_with_images[str(parent.relative_to(archive_path))] += 1

print("\nFolders containing images and their counts:")
for folder, count in sorted(folders_with_images.items()):
    print(f"  {folder}: {count} images")

# Check image formats and corrupted images
print("\nVerifying image integrity (checking first 500 or all if fast)...")
corrupt_count = 0
formats = defaultdict(int)

for i, img_path in enumerate(images_found):
    try:
        with Image.open(img_path) as img:
            formats[img.format] += 1
            img.verify() # verify integrity
    except Exception as e:
        corrupt_count += 1
        print(f"Corrupt image found: {img_path} - {e}")
    if (i + 1) % 2000 == 0:
        print(f"  Checked {i + 1}/{len(images_found)} images...")

print(f"\nImage format distribution: {dict(formats)}")
print(f"Corrupt/unreadable images: {corrupt_count}")
print("="*60)
