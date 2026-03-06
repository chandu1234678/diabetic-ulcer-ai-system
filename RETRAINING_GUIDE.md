# Production-Level Model Retraining Guide

## Problem

The current model is showing **false positives** - classifying normal feet as ulcers with high confidence. This guide walks through the complete retraining pipeline to fix this issue.

## Root Causes Addressed

1. **Weak Data Augmentation**: Original augmentation (only H-flip, V-flip) insufficient for generalization
2. **No Stratified Splits**: Random splits can create class imbalance between train/val/test
3. **No Class Weighting**: Doesn't penalize false positives enough
4. **No Validation Monitoring**: No early stopping to prevent overfitting
5. **Data Quality Issues**: Corrupted or mislabeled images in dataset

## Step-by-Step Process

### Step 1: Validate Data Quality

First, scan the dataset for corrupted, low-resolution, or problematic images:

```bash
cd backend
python ../scripts/validate_data_quality.py
```

This generates a report identifying:
- Corrupted images (can't be loaded)
- Low-resolution images (<128x128)
- Unusual dimensions
- Low-contrast images (may indicate mislabeling)

**Output**: `data_quality_report.json`

The script can optionally remove problematic images. Review the report first, then uncomment the removal section if needed.

### Step 2: Analyze Current Model's False Positives

Understand which normal images the current model misclassifies:

```bash
cd backend
python ../scripts/analyze_false_positives.py
```

This generates detailed analysis of:
- False positive rate and specificity
- Top high-confidence false positives
- Confidence distributions
- Sensitivity and specificity metrics

**Output**: `false_positive_analysis/false_positive_analysis.json`

Review the high-confidence false positives to understand patterns (e.g., redness, discoloration, specific lighting).

### Step 3: Retrain Model with Production Improvements

Run the production-level retraining script:

```bash
cd scripts
python retrain_production_model.py
```

The script implements major improvements:

#### Dataset Handling
- **Stratified Splits**: Ensures class balance across train/val/test
- **Proper Validation**: 80% train, 20% test → 75% train, 25% validation from training data
- **Data Validation**: Skips corrupted images, validates dimensions

#### Data Augmentation (MUCH STRONGER)
- Color jitter (±30% brightness, ±30% contrast, ±20% saturation, ±10% hue)
- Random rotation (±15°)
- Random affine (±10% translation, ±10% scale)
- Horizontal/vertical flips
- Gaussian blur (helps model not overfit to texture)
- Random erasing (teaches robustness to occlusion)

#### Model Improvements
- Added dropout (50%) before classification layer
- Uses ResNet50 with proper fine-tuning capability
- Class weighting to penalize false positives more

#### Training Process
- **Optimizer**: AdamW with weight decay (L2 regularization)
- **Learning Rate Scheduling**: ReduceLROnPlateau (divides by 2 on plateau)
- **Early Stopping**: Stops if validation loss doesn't improve for 15 epochs
- **Best Model Selection**: Saves model with lowest validation loss

**Outputs**:
- `model_weights/ulcer_detection_model_best.pth` - Best model (lowest val loss)
- `model_weights/ulcer_detection_model_production.pth` - Final trained model
- `model_weights/training_history.json` - Epoch-by-epoch metrics

### Step 4: Update Production Model

Replace the old model with the new production model:

```bash
# Backup old model
cp model_weights/cnn_ulcer_model.pth model_weights/cnn_ulcer_model_backup_$(date +%Y%m%d_%H%M%S).pth

# Use new model
cp model_weights/ulcer_detection_model_production.pth model_weights/cnn_ulcer_model.pth
```

### Step 5: Verify Improvements

Test the model on the same images that caused false positives:

```bash
cd backend
python ../scripts/analyze_false_positives.py
```

Compare metrics:
- **False Positive Rate**: Should significantly decrease
- **Specificity**: Should increase (better at identifying normal feet)
- **Confidence on FP**: High-confidence false positives should be minimized

## Key Metrics to Monitor

| Metric | What It Means | Target |
|--------|---------------|--------|
| **Sensitivity** | % of actual ulcers detected (recall) | >90% |
| **Specificity** | % of normal feet correctly identified | >95% |
| **False Positive Rate** | % of normal feet misclassified | <5% |
| **False Negative Rate** | % of ulcers missed | <10% |
| **Overall Accuracy** | % correct overall | >92% |

## Retraining Tips & Troubleshooting

### If Model Still Has False Positives

1. **Increase Augmentation Strength**
   - In `retrain_production_model.py`, increase `ColorJitter` values
   - Increase rotation angle
   - Increase `RandomErasing` probability

2. **Add More Data**
   - Collect additional "edge case" normal feet images
   - Focus on variations that cause false positives
   - Use synthetic data augmentation if needed

3. **Increase Class Weight**
   - Modify `compute_class_weights()` to weight normal class higher
   - This penalizes false positives more heavily

4. **Ensemble Models**
   - Train multiple models with different random seeds
   - Average predictions for more robust results

### If Training is Slow

- Reduce `batch_size` from 32 to 16 (trades accuracy for speed during training)
- Use fewer data augmentations
- Reduce `num_epochs` threshold

### If GPU Memory Issues

- Reduce `batch_size` to 16 or 8
- Use gradient accumulation
- Reduce model complexity (e.g., ResNet34 instead of ResNet50)

## File Structure

```
scripts/
├── retrain_production_model.py      # Main training script
├── validate_data_quality.py         # Data quality checker
├── analyze_false_positives.py       # FP analysis tool
├── train_cnn_model.py              # Original training (deprecated)
└── ...

model_weights/
├── cnn_ulcer_model.pth             # Current production model
├── cnn_ulcer_model_backup_*.pth   # Backups before retraining
├── ulcer_detection_model_best.pth  # Best from retraining
├── ulcer_detection_model_production.pth  # Final retrained model
└── training_history.json           # Metrics from latest training

data_quality_report.json            # From validate_data_quality.py
false_positive_analysis/            # From analyze_false_positives.py
├── false_positive_analysis.json
└── ...
```

## Expected Results

After proper retraining with the production script:

- **Specificity improvement**: 85% → 95%+ (fewer normal feet misclassified)
- **False positive rate**: 15% → 5% (major improvement)
- **Sensitivity maintained**: >90% (ulcers still detected)

## Continuous Improvement

1. **Collect User Feedback**: Log predictions that users dispute
2. **Regular Retraining**: Retrain monthly with new data
3. **Monitor Drift**: Track if FP rate increases over time
4. **A/B Testing**: Deploy new model alongside old, compare metrics

## Implementation in Code

To use the new model in the inference service:

```python
# In app/services/model_loader.py
model_path = "path/to/ulcer_detection_model_production.pth"
checkpoint = torch.load(model_path, map_location=device)
model.load_state_dict(checkpoint['model_state_dict'])
```

The model expects:
- Input: 224×224 RGB image
- Normalization: ImageNet stats (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
- Output: [P(normal), P(ulcer)] logits

---

**Questions?** Check the training_history.json and false_positive_analysis.json files for detailed metrics.
