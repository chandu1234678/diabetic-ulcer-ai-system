"""
Script to analyze false positives from the current model.
Helps identify which normal images are being misclassified as ulcers.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
import torchvision.transforms as transforms
from PIL import Image
import os
import numpy as np
import json
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SimpleImageDataset(Dataset):
    """Simple dataset for inference."""
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.images = []
        self.labels = []
        self.image_names = []
        
        self.transform = transform or transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        for label, class_name in enumerate(['normal', 'ulcers']):
            class_dir = os.path.join(root_dir, class_name)
            if os.path.exists(class_dir):
                for img_name in os.listdir(class_dir):
                    if img_name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                        self.images.append(os.path.join(class_dir, img_name))
                        self.labels.append(label)
                        self.image_names.append(f"{class_name}/{img_name}")
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        img_path = self.images[idx]
        image = Image.open(img_path).convert('RGB')
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
        
        return image, label, self.image_names[idx]


def analyze_false_positives(model_path, dataset_path, output_dir='false_positive_analysis'):
    """Analyze false positives in the current model."""
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    logger.info(f"Loading model from: {model_path}")
    logger.info(f"Device: {device}")
    
    # Define model class
    import torchvision.models as models
    
    class UlcerCNNModel(nn.Module):
        def __init__(self, num_classes=2, pretrained=True):
            super(UlcerCNNModel, self).__init__()
            self.resnet = models.resnet50(pretrained=pretrained)
            num_ftrs = self.resnet.fc.in_features
            self.resnet.fc = nn.Linear(num_ftrs, num_classes)
        
        def forward(self, x):
            return self.resnet(x)
    
    model = UlcerCNNModel(num_classes=2, pretrained=False)
    
    try:
        checkpoint = torch.load(model_path, map_location=device)
        
        if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
        else:
            model.load_state_dict(checkpoint)
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        logger.error("Model might not exist yet. Please train the model first.")
        return None
    
    model = model.to(device)
    model.eval()
    
    logger.info("Loading dataset...")
    dataset = SimpleImageDataset(dataset_path)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=False, num_workers=2)
    
    logger.info("Running inference...")
    
    analysis = {
        'false_positives': [],  # Normal classified as ulcer
        'false_negatives': [],  # Ulcer classified as normal
        'true_positives': [],
        'true_negatives': [],
        'confidence_distribution': {
            'fp': [],  # False positive confidences
            'fn': [],  # False negative confidences
            'tp': [],
            'tn': []
        },
        'summary': {}
    }
    
    total = 0
    correct = 0
    
    with torch.no_grad():
        for images, labels, image_names in dataloader:
            images = images.to(device)
            labels = labels.to(device)
            
            outputs = model(images)
            confidences = F.softmax(outputs, dim=1)
            _, predictions = torch.max(outputs, 1)
            
            # Process each prediction
            for idx in range(len(predictions)):
                pred = predictions[idx].item()
                true_label = labels[idx].item()
                confidence_ulcer = confidences[idx, 1].item()
                confidence_normal = confidences[idx, 0].item()
                img_name = image_names[idx]
                
                result = {
                    'image': img_name,
                    'true_label': 'normal' if true_label == 0 else 'ulcer',
                    'predicted_label': 'normal' if pred == 0 else 'ulcer',
                    'confidence_normal': float(confidence_normal),
                    'confidence_ulcer': float(confidence_ulcer),
                    'max_confidence': float(max(confidence_normal, confidence_ulcer))
                }
                
                total += 1
                
                if pred == true_label:
                    correct += 1
                    if true_label == 0:
                        analysis['true_negatives'].append(result)
                        analysis['confidence_distribution']['tn'].append(result['max_confidence'])
                    else:
                        analysis['true_positives'].append(result)
                        analysis['confidence_distribution']['tp'].append(result['max_confidence'])
                else:
                    if true_label == 0:  # Normal but predicted ulcer
                        analysis['false_positives'].append(result)
                        analysis['confidence_distribution']['fp'].append(result['confidence_ulcer'])
                    else:  # Ulcer but predicted normal
                        analysis['false_negatives'].append(result)
                        analysis['confidence_distribution']['fn'].append(result['confidence_normal'])
    
    # Summary statistics
    analysis['summary'] = {
        'total_samples': total,
        'accuracy': round(correct / total, 4),
        'false_positives': len(analysis['false_positives']),
        'false_positive_rate': round(len(analysis['false_positives']) / (len(analysis['false_positives']) + len(analysis['true_negatives'])) if (len(analysis['false_positives']) + len(analysis['true_negatives'])) > 0 else 0, 4),
        'false_negatives': len(analysis['false_negatives']),
        'false_negative_rate': round(len(analysis['false_negatives']) / (len(analysis['false_negatives']) + len(analysis['true_positives'])) if (len(analysis['false_negatives']) + len(analysis['true_positives'])) > 0 else 0, 4),
        'sensitivity': round(len(analysis['true_positives']) / (len(analysis['true_positives']) + len(analysis['false_negatives'])) if (len(analysis['true_positives']) + len(analysis['false_negatives'])) > 0 else 0, 4),
        'specificity': round(len(analysis['true_negatives']) / (len(analysis['true_negatives']) + len(analysis['false_positives'])) if (len(analysis['true_negatives']) + len(analysis['false_positives'])) > 0 else 0, 4),
    }
    
    # Log results
    logger.info("\n" + "="*60)
    logger.info("FALSE POSITIVE ANALYSIS")
    logger.info("="*60)
    logger.info(f"Total samples: {analysis['summary']['total_samples']}")
    logger.info(f"Overall accuracy: {analysis['summary']['accuracy']:.4f}")
    logger.info(f"\nFalse Positives (Normal → Ulcer): {analysis['summary']['false_positives']}")
    logger.info(f"False Positive Rate: {analysis['summary']['false_positive_rate']:.4f}")
    logger.info(f"\nFalse Negatives (Ulcer → Normal): {analysis['summary']['false_negatives']}")
    logger.info(f"False Negative Rate: {analysis['summary']['false_negative_rate']:.4f}")
    logger.info(f"\nSensitivity (True Positive Rate): {analysis['summary']['sensitivity']:.4f}")
    logger.info(f"Specificity (True Negative Rate): {analysis['summary']['specificity']:.4f}")
    
    # Sort false positives by confidence
    if analysis['false_positives']:
        logger.info(f"\n{'HIGH-CONFIDENCE FALSE POSITIVES (Most Concerning)':-^60}")
        sorted_fp = sorted(analysis['false_positives'], key=lambda x: x['confidence_ulcer'], reverse=True)
        for result in sorted_fp[:10]:
            logger.info(f"  {result['image']}: {result['confidence_ulcer']:.4f} confidence")
    
    # Save detailed analysis
    output_file = os.path.join(output_dir, 'false_positive_analysis.json')
    with open(output_file, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    logger.info(f"\nDetailed analysis saved to: {output_file}")
    
    # Create confidence distribution report
    logger.info(f"\n{'CONFIDENCE DISTRIBUTIONS':-^60}")
    for category, confidences in analysis['confidence_distribution'].items():
        if confidences:
            mean_conf = np.mean(confidences)
            std_conf = np.std(confidences)
            logger.info(f"  {category}: mean={mean_conf:.4f}, std={std_conf:.4f}, n={len(confidences)}")
    
    return analysis


if __name__ == "__main__":
    import os
    # Get project root dynamically
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    model_path = os.path.join(project_root, "model_weights", "cnn_ulcer_model.pth")
    dataset_path = os.path.join(project_root, "datasets", "images")
    
    logger.info(f"Model path: {model_path}")
    logger.info(f"Dataset path: {dataset_path}")
    
    if os.path.exists(model_path):
        analysis = analyze_false_positives(model_path, dataset_path)
        if analysis is None:
            logger.error("Failed to analyze false positives")
    else:
        logger.error(f"Model not found at: {model_path}")
        logger.error("Please train the model first using retrain_production_model.py")
