"""Evaluation script for trained models."""

import torch
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score
)
import json
import logging

logger = logging.getLogger(__name__)


def evaluate_model(model, test_loader, device, num_classes=3):
    """
    Evaluate model on test set.
    
    Args:
        model: PyTorch model
        test_loader: Test data loader
        device: Device (CPU/GPU)
        num_classes: Number of output classes
    
    Returns:
        Dictionary with evaluation metrics
    """
    
    model = model.to(device)
    model.eval()
    
    all_predictions = []
    all_targets = []
    all_probabilities = []
    
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            
            outputs = model(images)
            probabilities = torch.softmax(outputs, dim=1)
            predictions = outputs.argmax(dim=1)
            
            all_predictions.extend(predictions.cpu().numpy())
            all_targets.extend(labels.cpu().numpy())
            all_probabilities.extend(probabilities.cpu().numpy())
    
    all_predictions = np.array(all_predictions)
    all_targets = np.array(all_targets)
    all_probabilities = np.array(all_probabilities)
    
    # Compute metrics
    accuracy = accuracy_score(all_targets, all_predictions)
    precision = precision_score(
        all_targets, all_predictions, average='weighted', zero_division=0
    )
    recall = recall_score(
        all_targets, all_predictions, average='weighted', zero_division=0
    )
    f1 = f1_score(
        all_targets, all_predictions, average='weighted', zero_division=0
    )
    
    cm = confusion_matrix(all_targets, all_predictions)
    
    # Per-class metrics
    class_report = classification_report(
        all_targets, all_predictions, zero_division=0, output_dict=True
    )
    
    # AUC-ROC (for binary and multiclass)
    try:
        if num_classes == 2:
            auc_roc = roc_auc_score(all_targets, all_probabilities[:, 1])
        else:
            auc_roc = roc_auc_score(
                all_targets, all_probabilities, multi_class='ovr', zero_division=0
            )
    except:
        auc_roc = None
    
    metrics = {
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1),
        'auc_roc': float(auc_roc) if auc_roc is not None else None,
        'confusion_matrix': cm.tolist(),
        'class_report': class_report
    }
    
    logger.info(f"Accuracy: {accuracy:.4f}, Precision: {precision:.4f}, "
                f"Recall: {recall:.4f}, F1: {f1:.4f}")
    
    return metrics


def save_evaluation_report(metrics, output_path):
    """Save evaluation report to JSON."""
    with open(output_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    logger.info(f"Saved evaluation report to {output_path}")


def print_evaluation_report(metrics):
    """Print evaluation report to console."""
    print("\n" + "="*50)
    print("MODEL EVALUATION REPORT")
    print("="*50)
    print(f"Accuracy:  {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall:    {metrics['recall']:.4f}")
    print(f"F1-Score:  {metrics['f1_score']:.4f}")
    if metrics.get('auc_roc') is not None:
        print(f"AUC-ROC:   {metrics['auc_roc']:.4f}")
    print("\nConfusion Matrix:")
    print(np.array(metrics['confusion_matrix']))
    print("="*50 + "\n")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Model evaluation script initialized")
