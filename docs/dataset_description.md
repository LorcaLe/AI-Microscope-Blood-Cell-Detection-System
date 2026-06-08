# Dataset Description — BCCD Blood Cell Count and Detection Dataset

## Dataset Name

BCCD — Blood Cell Count and Detection Dataset

## Source

The dataset was provided as `archive.zip` and extracted into the project directory:

```text
data/raw/BCCD/
```

## Purpose of Use

This dataset is used for an object detection task on microscopic blood cell images. The model is expected to detect the position of each blood cell using bounding boxes and classify each detected object into one of three classes:

```text
Platelets
RBC
WBC
```

This dataset is suitable for the AI Microscope Blood Cell Detection System project, especially for the following workflow:

```text
Upload microscopic blood cell image
→ Detect blood cells
→ Draw bounding boxes
→ Count RBC / WBC / Platelets
```

## Number of Images

Based on the current extracted dataset:

```text
Train: 765 images
Validation: 73 images
Test: 36 images
Total: 874 images
```

Note: The dataset README may mention 364 images, but the current `archive.zip` version contains 874 images. This may be because the current dataset version was exported, processed, or augmented from another source.

## Number of Classes

The dataset contains 3 classes.

## Class Names

```text
0: Platelets
1: RBC
2: WBC
```

## Annotation Format

The dataset uses YOLO annotation format.

Each image in the `images/` folder has a corresponding `.txt` annotation file in the `labels/` folder.

Example:

```text
train/images/BloodImage_00001.jpg
train/labels/BloodImage_00001.txt
```

Each line in a YOLO label file follows this structure:

```text
class_id x_center y_center width height
```

Where:

```text
class_id   : the class ID of the detected object
x_center   : normalized x-coordinate of the bounding box center
y_center   : normalized y-coordinate of the bounding box center
width      : normalized width of the bounding box
height     : normalized height of the bounding box
```

The values of `x_center`, `y_center`, `width`, and `height` are normalized between 0 and 1.

## Observed Folder Structure

```text
data/raw/BCCD/
├── train/
│   ├── images/
│   └── labels/
├── valid/
│   ├── images/
│   └── labels/
├── test/
│   ├── images/
│   └── labels/
├── data.yaml
├── README.md
├── README.dataset.txt
└── LICENSE
```

## Observed Issues

1. The original `data.yaml` file may contain an absolute Windows path from the dataset creator's machine. It should be changed to a relative or project-specific path before training YOLO.

2. This dataset is not a classification dataset. It is an object detection dataset.

3. The annotation folder is named `labels/`, not `annotations/`, because the dataset follows the YOLO format.

4. The number of images mentioned in the README may not match the actual number of images in the extracted dataset.

5. The dataset is relatively small. It is suitable for learning object detection and building a prototype, but it should not be considered sufficient for a real clinical or medical diagnosis system.

## Recommended `data.yaml` Configuration

For this project, the `data.yaml` file should be configured as follows:

```yaml
path: D:/IT/AI Microscope Blood Cell Detection System/data/raw/BCCD

train: train/images
val: valid/images
test: test/images

names:
  0: Platelets
  1: RBC
  2: WBC
```

Note: Forward slashes `/` are recommended for Windows paths in YAML files to avoid escape path issues.

## YOLO Training Test

A YOLO11n model was trained for 1 epoch to verify that the dataset was correctly configured.

Training command:

```powershell
yolo detect train model=yolo11n.pt data="data/raw/BCCD/data.yaml" epochs=1 imgsz=416 batch=4
```

Training configuration:

```text
Model: yolo11n.pt
Epochs: 1
Image size: 416
Batch size: 4
Device: CPU
```

Dataset scan result:

```text
Train: 765 images, 0 corrupt
Validation: 73 images, 0 corrupt
```

Validation result after 1 epoch:

```text
Precision: 0.722
Recall: 0.724
mAP50: 0.798
mAP50-95: 0.506
```

Per-class results:

```text
Platelets:
Precision: 0.939
Recall: 0.201
mAP50: 0.618
mAP50-95: 0.281

RBC:
Precision: 0.359
Recall: 0.969
mAP50: 0.797
mAP50-95: 0.501

WBC:
Precision: 0.869
Recall: 1.000
mAP50: 0.979
mAP50-95: 0.736
```

Conclusion: The dataset is correctly configured and can be used for YOLO object detection training.

## YOLO Prediction Test

A prediction test was performed using the trained test model.

Prediction command:

```powershell
yolo detect predict model="models/bccd_yolo_test.pt" source="data/raw/BCCD/test/images/BloodImage_00113_jpg.rf.a17463f1ddc2e7729f935f8a74bc86a4.jpg" conf=0.25
```

Test image:

```text
BloodImage_00113_jpg.rf.a17463f1ddc2e7729f935f8a74bc86a4.jpg
```

Prediction result:

```text
RBC: 28
WBC: 1
Platelets: 0
```

Output result folder:

```text
runs/detect/predict-2/
```

Conclusion: The model was able to detect blood cells on a test image and generate bounding boxes with cell counts.

## Project Notes

This dataset will be used for the object detection phase of the AI Microscope Blood Cell Detection System project.

The first target is to train a YOLO model that can detect and count:

```text
Platelets
RBC
WBC
```

Expected model output:

```text
Input: microscopic blood cell image

Output:
- Bounding boxes around detected cells
- Class label for each detected cell
- Confidence score
- Number of Platelets
- Number of RBC
- Number of WBC
```

## Current Status

The dataset has been placed in the correct project folder, YOLO training has been tested successfully, and prediction on a test image has produced valid detection output.

The current model `bccd_yolo_test.pt` was trained for only 1 epoch and should be treated as a pipeline test model, not a final production model.

Next recommended step:

```text
Train YOLO11n for 10–30 epochs to improve detection performance.
```
