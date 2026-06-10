from pathlib import Path
import shutil


RAW_DIR = Path("data/raw/BCCD")
PROCESSED_DIR = Path("data/processed")


SPLIT_MAPPING = {
    "train": "train",
    "valid": "val",
    "test": "test"
}


CLASS_NAMES = {
    0: "Platelets",
    1: "RBC",
    2: "WBC"
}


def create_directories():
    for split in ["train", "val", "test"]:
        (PROCESSED_DIR / "images" / split).mkdir(parents=True, exist_ok=True)
        (PROCESSED_DIR / "labels" / split).mkdir(parents=True, exist_ok=True)


def copy_split(raw_split_name, processed_split_name):
    raw_image_dir = RAW_DIR / raw_split_name / "images"
    raw_label_dir = RAW_DIR / raw_split_name / "labels"

    processed_image_dir = PROCESSED_DIR / "images" / processed_split_name
    processed_label_dir = PROCESSED_DIR / "labels" / processed_split_name

    image_paths = list(raw_image_dir.glob("*.jpg")) + list(raw_image_dir.glob("*.png")) + list(raw_image_dir.glob("*.jpeg"))

    for image_path in image_paths:
        label_path = raw_label_dir / f"{image_path.stem}.txt"

        if not label_path.exists():
            print(f"Warning: missing label for {image_path.name}")
            continue

        shutil.copy2(image_path, processed_image_dir / image_path.name)
        shutil.copy2(label_path, processed_label_dir / label_path.name)

    print(f"Copied {len(image_paths)} images from {raw_split_name} to {processed_split_name}")


def create_data_yaml():
    yaml_content = """path: data/processed

train: images/train
val: images/val
test: images/test

names:
  0: Platelets
  1: RBC
  2: WBC
"""

    yaml_path = PROCESSED_DIR / "data.yaml"

    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(yaml_content)

    print(f"Created {yaml_path}")


def main():
    create_directories()

    for raw_split_name, processed_split_name in SPLIT_MAPPING.items():
        copy_split(raw_split_name, processed_split_name)

    create_data_yaml()

    print("Dataset has been prepared in data/processed/")


if __name__ == "__main__":
    main()