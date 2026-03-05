# Normal/Healthy Skin Images Dataset

This directory contains images of normal, healthy skin without ulcers.

## Directory Structure

- `training/`: Control images for model training
- `validation/`: Control images for validation
- `test/`: Control images for testing

## Purpose

These images serve as negative examples for:
- Binary classification (ulcer vs. no ulcer)
- Model validation and testing
- False positive analysis

## Image Requirements

- **Format**: JPG, PNG, or TIFF
- **Size**: 256x256 pixels (will be resized during preprocessing)
- **Color Space**: RGB
- **Quality**: High resolution clinical photos
- **Conditions**: Healthy skin without wounds, infections, or lesions

## Usage

Images are loaded alongside ulcer images for training balanced models:

```python
dataset = SkinImageDataset(
    ulcer_dir="datasets/images/ulcers",
    normal_dir="datasets/images/normal"
)
```

## Privacy and Ethics

- All patient images must be de-identified
- Obtain proper consent for image usage
- Follow institutional privacy policies
- Ensure geographic and demographic diversity

---

Note: Add actual control images according to your dataset collection protocols.
