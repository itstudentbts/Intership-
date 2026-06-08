import os
import shutil
import random

SOURCE_DIR = r"D:\cesi\ai food\Intership-\data\raw\food-101\food-101\food-101\images"
TRAIN_DIR  = r"D:\cesi\ai food\Intership-\data\processed\train"
VAL_DIR    = r"D:\cesi\ai food\Intership-\data\processed\val"
TEST_DIR   = r"D:\cesi\ai food\Intership-\data\processed\test"

# only 10 classes to start — faster to train
CLASSES = [
    "pizza",
    "sushi",
    "hamburger",
    "ramen",
    "steak",
    "donuts",
    "french_fries",
    "ice_cream",
    "hot_dog",
    "chocolate_cake"
]

def organise():
    # create folders
    for folder in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
        for cls in CLASSES:
            os.makedirs(os.path.join(folder, cls), exist_ok=True)
    print("Folders created")

    for cls in CLASSES:
        src = os.path.join(SOURCE_DIR, cls)
        if not os.path.exists(src):
            print(f"NOT FOUND: {cls}")
            continue

        # get real images only — skip Mac ._files
        images = [f for f in os.listdir(src)
                  if f.endswith('.jpg')
                  and not f.startswith('._')]
        random.shuffle(images)

        # split 70/15/15
        total     = len(images)
        train_end = int(total * 0.70)
        val_end   = train_end + int(total * 0.15)

        splits = {
            TRAIN_DIR: images[:train_end],
            VAL_DIR:   images[train_end:val_end],
            TEST_DIR:  images[val_end:]
        }

        for dest, files in splits.items():
            for f in files:
                shutil.copy(
                    os.path.join(src, f),
                    os.path.join(dest, cls, f)
                )

        print(f"✅ {cls}: {train_end} train | "
              f"{val_end-train_end} val | "
              f"{total-val_end} test")

    print("\nDone!")

if __name__ == "__main__":
    organise()