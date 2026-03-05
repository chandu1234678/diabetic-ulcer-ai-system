# Datasets

This directory contains all training, validation, and test datasets for the Diabetic Ulcer AI System.

## Structure

```
datasets/
├── images/
│   ├── ulcers/              # Images with ulcers
│   └── normal/              # Images without ulcers
├── segmentation_masks/      # Binary masks for segmentation
└── clinical_data/
    └── patient_data.csv     # Clinical patient information
```

## Image Dataset

### Ulcers Directory
Contains images of diabetic ulcers captured from various angles and lighting conditions.
- Format: JPEG, PNG, TIFF
- Resolution: 512x512 to 2048x2048 pixels
- Count: ~500 images

### Normal Directory
Contains images of healthy skin without ulcers.
- Format: JPEG, PNG, TIFF
- Resolution: 512x512 to 2048x2048 pixels
- Count: ~500 images

## Segmentation Masks

Binary masks indicating ulcer regions:
- Format: PNG (8-bit grayscale)
- 0 = Non-ulcer region
- 255 = Ulcer region
- One mask per corresponding image

## Clinical Data (patient_data.csv)

Patient clinical information including:
- patient_id: Unique patient identifier
- age: Patient age in years
- gender: M/F
- diabetes_type: Type 1, Type 2, Gestational
- duration_years: Years since diabetes diagnosis
- hba1c_level: Glycemic control measure
- bmi: Body Mass Index
- smoking_status: Never/Former/Active
- neuropathy: Presence of peripheral neuropathy
- previous_ulcers: Number of previous ulcers

## Data Splits

For training/validation/testing:
- Training: 70% of data
- Validation: 15% of data
- Testing: 15% of data

## Privacy Notes

All patient data is anonymized with sequential IDs.
No personally identifiable information is included.

## Download Instructions

Most datasets are too large for Git. Download from:
- Main dataset: [Link to dataset storage]
- checksum files available for verification
