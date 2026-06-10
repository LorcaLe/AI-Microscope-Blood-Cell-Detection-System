from pathlib import Path
import random
import shutil


RAW_IMAGE_DIR = Path("data/raw/images")
RAW_LABEL_DIR = Path("data/raw/labels")
OUTPUT_DIR = Path("data/processed")

TRAIN_RATIO = 0.7
VAL_RATIO = 0.2
TEST_RATIO = 0.1

RANDOM_SEED = 42


def create_output_dirs():
    for split in ["train", "val", "test"]:
        (OUTPUT_DIR / "images" / split).mkdir(parents=True, exist_ok=True)
        (OUTPUT_DIR / "labels" / split).mkdir(parents=True, exist_ok=True)


def split_items(items):
    random.seed(RANDOM_SEED)
    random.shuffle(items)

    total = len(items)

    train_end = int(total * TRAIN_RATIO)
    val_end = train_end + int(total * VAL_RATIO)

    train_items = items[:train_end]
    val_items = items[train_end:val_end]
    test_items = items[val_end:]

    return train_items, val_items, test_items


def copy_items(items, split):
    for image_path in items:
        label_path = RAW_LABEL_DIR / f"{image_path.stem}.txt"

        if not label_path.exists():
            print(f"Missing label: {label_path}")
            continue

        shutil.copy2(image_path, OUTPUT_DIR / "images" / split / image_path.name)
        shutil.copy2(label_path, OUTPUT_DIR / "labels" / split / label_path.name)


def main():
    print("This script is for datasets that are not already split.")
    print("Your current BCCD dataset already has train/valid/test folders.")
    print("Use src/data/convert_to_yolo.py instead for this project.")

    if not RAW_IMAGE_DIR.exists() or not RAW_LABEL_DIR.exists():
        print("Raw images/labels folder not found. Skipping split.")
        return

    create_output_dirs()

    image_paths = list(RAW_IMAGE_DIR.glob("*.jpg")) + list(RAW_IMAGE_DIR.glob("*.png")) + list(RAW_IMAGE_DIR.glob("*.jpeg"))

    train_items, val_items, test_items = split_items(image_paths)

    copy_items(train_items, "train")
    copy_items(val_items, "val")
    copy_items(test_items, "test")

    print("Split completed.")
    print("Train:", len(train_items))
    print("Val:", len(val_items))
    print("Test:", len(test_items))


if __name__ == "__main__":
    main()