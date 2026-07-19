"""
organise_data_101.py
====================
Splits all 101 Food-101 classes into train / val / test folders.
Run this BEFORE train_model_101.py
"""

import os
import shutil
import random

# ══════════════════════════════════════════════════════════
# SETTINGS — update SOURCE_DIR to your food-101 images path
# ══════════════════════════════════════════════════════════

SOURCE_DIR = r"D:\cesi\ai food\Intership-\data\raw\food-101\food-101\food-101\images"
TRAIN_DIR  = r"D:\cesi\ai food\Intership-\data\processed\train"
VAL_DIR    = r"D:\cesi\ai food\Intership-\data\processed\val"
TEST_DIR   = r"D:\cesi\ai food\Intership-\data\processed\test"

TRAIN_SPLIT = 0.70   # 70% training
VAL_SPLIT   = 0.15   # 15% validation
TEST_SPLIT  = 0.15   # 15% test

# ══════════════════════════════════════════════════════════


def get_all_classes(source_dir):
    """Get all 101 class folder names from Food-101."""
    if not os.path.exists(source_dir):
        print(f"ERROR: SOURCE_DIR not found: {source_dir}")
        print("Update SOURCE_DIR in this script to your food-101/images path")
        return []

    classes = [
        d for d in sorted(os.listdir(source_dir))
        if os.path.isdir(os.path.join(source_dir, d))
        and not d.startswith('.')
        and not d.startswith('_')
    ]
    return classes


def create_folders(classes):
    """Create train/val/test folder for every class."""
    for split_dir in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
        for cls in classes:
            os.makedirs(os.path.join(split_dir, cls), exist_ok=True)
    print(f"Created folders for {len(classes)} classes")


def organise_class(cls):
    """
    Copy images for one class into train/val/test splits.
    Skips Mac ._files automatically.
    Returns (class_name, train_count, val_count, test_count)
    """
    src = os.path.join(SOURCE_DIR, cls)

    if not os.path.exists(src):
        return cls, 0, 0, 0

    # get real jpg images only — skip Mac ._files
    images = [
        f for f in os.listdir(src)
        if f.lower().endswith('.jpg')
        and not f.startswith('._')
    ]

    if not images:
        print(f"  WARNING: No images found for {cls}")
        return cls, 0, 0, 0

    random.shuffle(images)

    total     = len(images)
    train_end = int(total * TRAIN_SPLIT)
    val_end   = train_end + int(total * VAL_SPLIT)

    splits = {
        TRAIN_DIR: images[:train_end],
        VAL_DIR:   images[train_end:val_end],
        TEST_DIR:  images[val_end:]
    }

    for dest_dir, files in splits.items():
        for f in files:
            src_path  = os.path.join(src, f)
            dest_path = os.path.join(dest_dir, cls, f)
            if not os.path.exists(dest_path):
                shutil.copy(src_path, dest_path)

    train_c = len(splits[TRAIN_DIR])
    val_c   = len(splits[VAL_DIR])
    test_c  = len(splits[TEST_DIR])

    return cls, train_c, val_c, test_c


def check_existing():
    """Check how many classes are already processed."""
    if not os.path.exists(TRAIN_DIR):
        return 0
    existing = [
        d for d in os.listdir(TRAIN_DIR)
        if os.path.isdir(os.path.join(TRAIN_DIR, d))
    ]
    return len(existing)


def main():
    print("=" * 55)
    print("  FOOD-101 DATA ORGANISATION — ALL 101 CLASSES")
    print("=" * 55)

    # check existing
    existing = check_existing()
    if existing > 0:
        print(f"\nFound {existing} classes already processed.")
        answer = input(
            "Do you want to skip already-done classes? (y/n): "
        ).strip().lower()
        skip_existing = (answer == 'y')
    else:
        skip_existing = False

    # get all 101 classes
    print(f"\nScanning: {SOURCE_DIR}")
    classes = get_all_classes(SOURCE_DIR)

    if not classes:
        print("No classes found. Check your SOURCE_DIR path.")
        return

    print(f"Found {len(classes)} food classes")
    print(f"First 5: {classes[:5]}")
    print(f"Last 5:  {classes[-5:]}")

    # create all folders
    create_folders(classes)

    # process each class
    print("\nCopying images...")
    print("-" * 50)

    total_train = total_val = total_test = 0
    skipped = 0

    for i, cls in enumerate(classes):

        # skip if already done
        if skip_existing:
            cls_train = os.path.join(TRAIN_DIR, cls)
            if os.path.exists(cls_train):
                existing_imgs = len(os.listdir(cls_train))
                if existing_imgs > 100:
                    skipped += 1
                    continue

        cls_name, tr, va, te = organise_class(cls)

        total_train += tr
        total_val   += va
        total_test  += te

        # print progress every 10 classes
        if (i + 1) % 10 == 0 or i == 0 or i == len(classes) - 1:
            print(
                f"[{i+1:3d}/101] {cls_name:<25} "
                f"train:{tr} val:{va} test:{te}"
            )

    # summary
    print("\n" + "=" * 55)
    print("DONE!")
    print(f"Classes processed:  {len(classes) - skipped}")
    print(f"Classes skipped:    {skipped}")
    print(f"Total train images: {total_train:,}")
    print(f"Total val images:   {total_val:,}")
    print(f"Total test images:  {total_test:,}")
    print(f"Total images:       {total_train + total_val + total_test:,}")
    print("=" * 55)
    print("\nNow run: python src/train_model_101.py")


if __name__ == "__main__":
    random.seed(42)   # reproducible splits
    main()
