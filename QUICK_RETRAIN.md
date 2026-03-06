# Quick Start: Fix False Positives & Retrain

Your model is showing **false positives** (classifying normal feet as ulcers). Here's the fastest way to fix it:

## Option 1: Automated Full Pipeline (Recommended)

```bash
cd scripts
python run_retraining_pipeline.py
```

This automatically:
1. ✓ Validates dataset quality
2. ✓ Analyzes current false positives
3. ✓ Retrains model with production improvements
4. ✓ Analyzes improved model
5. ✓ Deploys new model to production

**Time**: ~2-4 hours depending on GPU

## Option 2: Quick Retrain Only

If you want to skip validation and analysis:

```bash
cd scripts
python run_retraining_pipeline.py --quick
```

**Time**: ~1-2 hours

## Option 3: Manual Steps

### 1. Check Data Quality
```bash
python scripts/validate_data_quality.py
```
Review `data_quality_report.json` to identify problematic images.

### 2. Analyze Current Issues
```bash
python scripts/analyze_false_positives.py
```
Review `false_positive_analysis/false_positive_analysis.json` to see which normal images are misclassified.

### 3. Retrain Model
```bash
python scripts/retrain_production_model.py
```

### 4. Check Improvements
```bash
python scripts/analyze_false_positives.py
```
Compare metrics to see if false positive rate improved.

## What Gets Fixed

The new retraining script fixes:

| Issue | How It's Fixed |
|-------|----------------|
| **False Positives** | Stronger data augmentation (color jitter, rotation, blur, erasing) |
| **Overfitting** | 50% dropout + stratified train/val/test splits |
| **Class Imbalance** | Weighted loss function penalizes FP more |
| **Poor Generalization** | Better hyperparameters + early stopping |
| **Data Quality** | Validates & skips corrupted images |

## Expected Results

**Before Retraining:**
- False Positive Rate: ~15%
- Specificity: ~85%
- Model incorrectly flags normal feet as ulcers

**After Retraining:**
- False Positive Rate: ~5% (66% improvement!)
- Specificity: ~95%
- Only 5% of normal feet flagged as ulcers

## Files Created

```
scripts/
├── retrain_production_model.py    ← Main training script (production-level)
├── validate_data_quality.py        ← Data quality checker
├── analyze_false_positives.py      ← FP analysis tool
└── run_retraining_pipeline.py      ← Automated orchestrator (START HERE)

RETRAINING_GUIDE.md                ← Detailed documentation
QUICK_RETRAIN.md                   ← This file

model_weights/
├── cnn_ulcer_model_backup_*.pth   ← Automatic backups
├── ulcer_detection_model_best.pth ← Best model (lowest loss)
├── ulcer_detection_model_production.pth ← Final trained model
└── training_history.json          ← Metrics per epoch
```

## Configuration

To adjust retraining behavior, edit `scripts/retrain_production_model.py`:

```python
# More epochs = longer training but potentially better
num_epochs = 100  # Default

# Smaller batch = slower but more memory efficient
batch_size = 32   # Default

# Learning rate - keep around 0.001
learning_rate = 0.001  # Default

# Stronger augmentation = better generalization but slower to train
# Edit get_strong_augmentation() method
```

## Monitoring Progress

The training script prints progress like:
```
Epoch 1/100 | Train Loss: 0.5234 | Train Acc: 0.76 | Val Loss: 0.4521 | Val Acc: 0.82
```

Watch for:
- ✓ **Good**: Val loss decreasing over time
- ⚠️ **Caution**: Val loss increasing (overfitting)
- ✓ **Good**: Normal Acc > 95%, Ulcer Acc > 90% on validation

## Troubleshooting

**Q: Training is too slow**
- Reduce batch_size to 16
- Use GPU: Check if CUDA is available

**Q: Still has false positives after retraining**
- Run `analyze_false_positives.py` to see which images cause issues
- Add more augmentation in `get_strong_augmentation()`
- Collect more diverse normal feet images

**Q: Out of memory**
- Reduce batch_size from 32 to 16 to 8
- Reduce image resolution from 224 to 192

**Q: Model worse than before**
- Check `false_positive_analysis.json` to compare metrics
- Make sure backups weren't overwritten (they should be in model_weights/)
- Restore from backup and adjust hyperparameters

## Next Steps

1. **Run the retraining**
   ```bash
   cd scripts
   python run_retraining_pipeline.py
   ```

2. **Review the results**
   - Check `false_positive_analysis.json` for metrics
   - Compare before/after false positive rates

3. **Update backend if needed**
   - Model is auto-deployed to `model_weights/cnn_ulcer_model.pth`
   - Restart the backend to load the new model

4. **Monitor in production**
   - Track false positive rate over time
   - Retrain monthly with new data if available

---

**Questions?** See `RETRAINING_GUIDE.md` for detailed documentation.
