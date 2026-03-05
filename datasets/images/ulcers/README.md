# Ulcer Images Dataset

This directory contains training and testing images of diabetic ulcers.

## Directory Structure

- `training/`: Images used for model training
- `validation/`: Images used for validation
- `test/`: Images used for testing

## Image Requirements

- **Format**: JPG, PNG, or TIFF
- **Size**: 256x256 pixels (will be resized during preprocessing)
- **Color Space**: RGB
- **Quality**: High resolution clinical photos

## Data Preparation

1. Place images in their respective subdirectories
2. Ensure images are properly labeled
3. Run preprocessing pipeline before training

## Usage

Images are automatically loaded by the `UlcerSegmentationDataset` class in training scripts.

```python
from app.db.models import UlcerImage
dataset = UlcerSegmentationDataset("datasets/images/ulcers", "datasets/segmentation_masks")
```

## Privacy and Ethics

- All patient images must be de-identified
- Use only with proper ethical approval
- Follow HIPAA/regional privacy regulations
- Ensure informed consent for data usage

---

Note: Add actual training data according to your data collection protocols.
