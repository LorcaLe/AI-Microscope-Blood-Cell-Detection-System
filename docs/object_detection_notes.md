# Object Detection Notes

## How is Object Detection different from Image Classification?

**Image Classification** looks at the whole image and answers: *"What is in this image?"*
- Input: one image
- Output: one label
- Example: "This image contains a blood cell."

**Object Detection** looks at the image and answers: *"What is here, and exactly where is it?"*
- Input: one image
- Output: multiple bounding boxes + labels + confidence scores
- Example: "There are 312 RBCs at these locations, 8 WBCs at these locations, 45 Platelets at these locations."

In short: Classification = **what**. Detection = **what + where + how many**.

For blood cell analysis, classification is not enough — we need to count each type and locate them precisely. That is why object detection is the right approach.

---

## What is a Bounding Box?

A bounding box is a rectangle drawn around a detected object in an image.

It is defined by two corner points:
- Top-left corner: (x1, y1)
- Bottom-right corner: (x2, y2)

Every detected blood cell gets its own bounding box. The box tells us exactly where in the image the cell is located. Without bounding boxes, we would know a cell exists but not where it is.

---

## What is IoU?

IoU stands for **Intersection over Union**.

It measures how much the predicted bounding box overlaps with the ground truth box (the correct box drawn by a human).

```
IoU = Overlap area / Total combined area
```

| IoU Value | Meaning |
|---|---|
| 1.0 | Perfect — predicted box matches exactly |
| 0.5 | Acceptable — commonly used as the passing threshold |
| 0.0 | No overlap at all — completely wrong prediction |

IoU tells us whether the model found the object in the right place, not just whether it found the right class.

---

## What is mAP?

mAP stands for **Mean Average Precision**.

It is the main metric used to measure how good an object detection model is overall.

- It is calculated across all classes (RBC, WBC, Platelet) and all confidence thresholds
- The result is a single number between 0 and 1 (or 0% to 100%)
- Higher mAP = better model

```
mAP@0.5 = 0.85  →  very good model
mAP@0.5 = 0.45  →  needs more training
```

Think of mAP as the final exam score of your model. It summarizes performance in one number.

---

## Why are Precision and Recall important in biomedicine?

**Precision** — of all the cells the model detected, how many were real?

```
Precision = True Positives / (True Positives + False Positives)
```

Low precision means the model detects things that are not actually cells — false alarms.

**Recall** — of all the real cells in the image, how many did the model find?

```
Recall = True Positives / (True Positives + False Negatives)
```

Low recall means the model misses real cells — undetected objects.

---

### Why both matter in biomedicine:

In a normal app, a false alarm is just annoying. In medicine, both types of errors have real consequences:

| Error type | What happens | Medical consequence |
|---|---|---|
| Low Precision | Model detects fake cells | Doctor wastes time reviewing false results |
| Low Recall | Model misses real cells | Doctor misses a real diagnosis |

**Recall is usually more critical in medical AI.**

Missing a real abnormal WBC (which could indicate leukemia) is far more dangerous than having a few false alarms. A missed diagnosis can cost a patient's life.

This is why medical AI systems are designed to prioritize high recall, even if it means slightly lower precision — it is safer to flag too many things than to miss something important.
