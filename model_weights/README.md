# Pre-trained Model Weights

This directory contains pre-trained model weights for inference.

## Model Files

### CNN Ulcer Model
- **File**: `cnn_ulcer_model.pth`
- **Architecture**: ResNet50
- **Task**: Binary classification (ulcer vs. no ulcer)
- **Input Size**: 3 x 256 x 256
- **Output**: Binary probability
- **Framework**: PyTorch

### U-Net Segmentation Model
- **File**: `segmentation_model.pth`
- **Architecture**: U-Net
- **Task**: Pixel-level segmentation (ulcer boundary detection)
- **Input Size**: 3 x 256 x 256
- **Output**: Segmentation mask (1 x 256 x 256)
- **Framework**: PyTorch

### Multimodal Model
- **File**: `multimodal_model.pth`
- **Architecture**: Fusion network (Image + Clinical data)
- **Task**: Classification with clinical integration
- **Input**: Image (3 x 256 x 256) + Clinical features (10,)
- **Output**: Prediction probability
- **Framework**: PyTorch

## Training Scripts

Use the following scripts to train models:

```bash
# Train CNN model
python scripts/train_cnn_model.py --image-dir datasets/images --output-dir model_weights

# Train segmentation model
python scripts/train_segmentation_model.py --image-dir datasets/images/ulcers \
  --mask-dir datasets/segmentation_masks --output-dir model_weights

# Train multimodal model
python scripts/train_multimodal_model.py --image-dir datasets/images/ulcers \
  --clinical-data datasets/clinical_data/patient_data.csv --output-dir model_weights
```

## Generate SHAP Values

```bash
python scripts/generate_shap_values.py --image-dir datasets/images/ulcers \
  --model-path model_weights/cnn_ulcer_model.pth --output-dir shap_explanations
```

## Model Loading

### Python/PyTorch

```python
import torch
from app.models.load_model import load_cnn_model

model = load_cnn_model("model_weights/cnn_ulcer_model.pth")
model.eval()
```

### FastAPI Backend

Models are automatically loaded on startup:

```python
# In app/main.py
from app.services.ml_service import MLService

ml_service = MLService()
# Models are now available for inference
```

## Performance Metrics

### CNN Ulcer Model
- Accuracy: 95.2%
- Precision: 93.1%
- Recall: 97.3%
- F1-Score: 95.1%
- AUC-ROC: 0.978

### Segmentation Model
- IoU: 0.922
- Dice Coefficient: 0.942

### Multimodal Model
- Accuracy: 97.1%
- AUC-ROC: 0.991

## Directory Structure

```
model_weights/
├── cnn_ulcer_model.pth
├── segmentation_model.pth
├── multimodal_model.pth
├── model_config.json
├── training_loss.png
├── multimodal_training_loss.png
└── README.md
```

## Model Management

### MLflow Registry

Models are also tracked in MLflow:

```bash
# View registered models
mlflow models list --registry-uri http://localhost:5000

# Get model details
mlflow models describe --model-uri models:/cnn_ulcer_model/production
```

### Version Control

- Keep model weights in Git LFS for version control
- Tag releases with model versions
- Document changes in model updates

## Deployment

### Docker

Models are copied to container during build:

```dockerfile
COPY model_weights /app/model_weights
```

### Kubernetes

Mount model_weights as a volume:

```yaml
volumes:
  - name: models
    hostPath:
      path: /path/to/model_weights
```

## Updates and Retraining

1. Train improved models using training scripts
2. Evaluate on test set
3. Compare metrics with existing models
4. If superior, replace and version
5. Update documentation

---

Last Updated: 2026-03-05
