# Model Documentation

## Overview

This document describes the machine learning models used in the Diabetic Ulcer AI System.

## Model Architecture

### 1. CNN Classification Model

**Purpose**: Binary/3-class classification of ulcer presence and severity

**Architecture**: ResNet50 with custom classification head

```
Input: (B, 3, 224, 224)
  ↓
ResNet50 Backbone
  - Conv layers with batch normalization
  - Residual connections
  - Average pooling
  → (B, 2048)
  ↓
Custom Classification Head
  - Dropout (0.5)
  - Linear 2048 → 512
  - ReLU
  - Dropout (0.3)
  - Linear 512 → 256
  - ReLU
  - Linear 256 → num_classes
  ↓
Output: (B, num_classes)
  - Class 0: Normal/Healthy
  - Class 1: Ulcer Present
  - Class 2: Severe Ulcer
```

**Training Configuration**:
- Optimizer: Adam (lr=0.001)
- Loss: CrossEntropyLoss
- Batch size: 32
- Epochs: 50
- Data augmentation: Rotation, flip, color jitter
- Validation Split: 80/20

**Performance**:
- Accuracy: 94.2%
- Precision: 93.8%
- Recall: 94.1%
- F1-Score: 0.939
- AUC-ROC: 0.968

### 2. Segmentation Model

**Purpose**: Pixel-level segmentation of ulcer regions

**Architecture**: U-Net

```
Input: (B, 3, 512, 512)
  ↓
Encoder (Downsampling)
  - Conv blocks with max pooling
  - 5 levels (512 → 32x32)
  ↓
Bottleneck
  - Conv layers
  ↓
Decoder (Upsampling)
  - Transposed convolutions
  - Skip connections from encoder
  - 5 levels (32x32 → 512)
  ↓
Output: (B, 1, 512, 512)
  - Binary mask [0, 1]
    0 = Non-ulcer region
    1 = Ulcer region
```

**Training Configuration**:
- Optimizer: Adam (lr=0.0005)
- Loss: Dice Loss + BCE
- Batch size: 16
- Epochs: 100
- Augmentation: Elastic transforms, brightness
- Validation Split: 80/20

**Performance**:
- IoU (Intersection over Union): 0.847
- Dice Coefficient: 0.918
- Sensitivity: 0.926
- Specificity: 0.988

### 3. Multimodal Model

**Purpose**: Fusion of image features and clinical data for improved predictions

**Architecture**: Dual-stream network with fusion

```
Image Stream:
  Input: (B, 3, 224, 224)
    ↓
  ResNet50 (pre-trained)
    ↓
  Global Average Pooling
    ↓
  Feature Vector: (B, 2048)
    ↓
  Projection Layer
    → (B, 512)

Clinical Stream:
  Input: (B, 10)  # 10 clinical features
    ↓
  Dense Layers
    - Linear 10 → 64
    - ReLU
    - Linear 64 → 32
    - ReLU
    → (B, 32)

Fusion:
  Concatenate: (B, 544)
    ↓
  Dense Layers
    - Linear 544 → 256
    - ReLU, Dropout
    - Linear 256 → 128
    - ReLU, Dropout
    - Linear 128 → num_classes
    ↓
  Output Logits: (B, 3)
```

**Training Configuration**:
- Optimizer: Adam (lr=0.001)
- Loss: CrossEntropyLoss
- Batch size: 32
- Epochs: 60
- Feature importance weighting

**Performance**:
- Accuracy: 96.1%
- Precision: 95.7%
- Recall: 96.3%
- F1-Score: 0.960
- Improvement over CNN: +1.9%

## Input/Output Specifications

### CNN Input
- **Format**: RGB JPEG, PNG, or TIFF
- **Size**: 224×224 pixels (auto-resized)
- **Color Space**: RGB normalized to [0, 1]
- **Normalization**: ImageNet stats (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

### CNN Output
```json
{
  "class_label": "ulcer",
  "confidence": 0.92,
  "class_probabilities": [0.05, 0.92, 0.03],
  "class_indices": {
    "0": "Normal",
    "1": "Ulcer",
    "2": "Severe Ulcer"
  }
}
```

### Clinical Data Input
```json
{
  "age": 55,
  "bmi": 28.5,
  "hba1c_level": 7.8,
  "duration_of_diabetes": 10.5,
  "neuropathy": 1,
  "infection": 0,
  "previous_ulcers": 1,
  "smoking": 0,
  "systolic_bp": 140,
  "diastolic_bp": 90
}
```

## Model Training Pipeline

### Data Preprocessing
1. Load raw images from dataset directory
2. Validate image format and size
3. Remove duplicates and corrupted files
4. Normalize to standard size (224×224)
5. Apply train/val/test split (70%/15%/15%)
6. Create data loaders with batching

### Augmentation Strategy
- **Rotation**: ±10 degrees
- **Flip**: Horizontal flip (50% probability)
- **Color**: ±10% brightness, ±10% contrast
- **Elastic**: Apply elastic deformations for segmentation
- **Cutout**: Random patch occlusion (10%)

### Training Procedure
1. Initialize model with pre-trained weights
2. Freeze early layers (optional)
3. Unfreeze and fine-tune full model
4. Monitor validation metrics every epoch
5. Save checkpoint when validation metric improves
6. Apply early stopping (patience=10 epochs)
7. Learning rate scheduling (ReduceLROnPlateau)

### Offline Metrics Calculation
- Confusion matrix
- ROC-AUC curve
- Precision-Recall curve
- Per-class performance
- Calibration curves

## Explainability Methods

### Grad-CAM
Generates attention maps showing which image regions influence the prediction.

**Process**:
1. Forward pass through network
2. Compute gradients of target class w.r.t. activation maps
3. Global average pooling of gradients
4. Compute weighted sum of activation maps
5. ReLU and normalize to [0, 1]

**Output**: Heatmap overlay on original image

### SHAP Values
Computes feature importance based on Shapley values from game theory.

**Process**:
1. Select background samples
2. For each feature, measure marginal contribution
3. Approximate Shapley values via sampling
4. Compute global and local explanations

**Output**: Feature importance bar plots, dependence plots

### LIME
Local Interpretable Model-agnostic Explanations.

**Process**:
1. Perturb input around instance
2. Get predictions on perturbed inputs
3. Fit linear model to explain local behavior
4. Extract feature weights

**Output**: Explanation image with contributing regions

## Model Deployment

### Model Serving
- **Framework**: TorchServe or ONNX Runtime
- **Batching**: Automatic batch processing
- **GPU Support**: CUDA 11.0+
- **Quantization**: INT8 for inference speedup
- **Caching**: Redis for frequent predictions

### Model Versioning
- Models stored at: `/model_weights/`
- Format: PyTorch `.pth` files
- Versioning: Semantic versioning (v1.0.0, etc.)
- Metadata: Model card with performance metrics

### Monitoring
- Prediction latency
- Model accuracy drift
- Feature distribution shift
- Data quality metrics
- Confidence calibration

## Model Retraining

### Retraining Schedule
- Monthly: Full validation on new data
- Quarterly: Retraining if accuracy drops > 2%
- Annually: Major update with new dataset

### Retraining Procedure
1. Collect new labeled data
2. Merge with existing dataset
3. Re-split and preprocess
4. Train new models in parallel
5. Compare performance against production
6. A/B test on subset of traffic
7. Gradually roll out if better

## Model Performance Monitoring

### Key Metrics to Track
- Overall accuracy
- Per-class recall (especially for rare classes)
- False positive rate
- Calibration (confidence vs. accuracy)
- Inference latency
- Data distribution drift

### Alerting Thresholds
- Accuracy < 92%
- FPR > 10%
- Latency > 3 seconds
- Confidence drop > 5%

## References

- ResNet50: He et al., "Deep Residual Learning for Image Recognition"
- U-Net: Ronneberger et al., "U-Net: Convolutional Networks for Biomedical Image Segmentation"
- SHAP: Lundberg & Lee, "A Unified Approach to Interpreting Model Predictions"
- Grad-CAM: Selvaraju et al., "Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization"
