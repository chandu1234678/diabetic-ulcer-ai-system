"""
Production-level retraining script for diabetic ulcer detection model.
Addresses false positives by implementing:
- Stronger data augmentation
- Proper train/val/test stratified split
- Class weighting
- Early stopping
- Validation-based model selection
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import os
import json
import numpy as np
from pathlib import Path
from datetime import datetime
import logging
from sklearn.model_selection import StratifiedShuffleSplit

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class UlcerDatasetProduction(torch.utils.data.Dataset):
    """Enhanced dataset loader with stratified splitting capability."""
    
    def __init__(self, root_dir, indices=None, transform=None):
        self.root_dir = root_dir
        self.transform = transform or self.get_strong_augmentation()
        self.images = []
        self.labels = []
        
        self._load_images()
        
        if indices is not None:
            self.images = [self.images[i] for i in indices]
            self.labels = [self.labels[i] for i in indices]
    
    def _load_images(self):
        """Load images and ensure data quality."""
        for label, class_name in enumerate(['normal', 'ulcers']):
            class_dir = os.path.join(self.root_dir, class_name)
            if os.path.exists(class_dir):
                for img_name in os.listdir(class_dir):
                    if img_name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
                        img_path = os.path.join(class_dir, img_name)
                        try:
                            # Validate image can be opened
                            with Image.open(img_path) as img:
                                if img.size[0] >= 128 and img.size[1] >= 128:  # Min size validation
                                    self.images.append(img_path)
                                    self.labels.append(label)
                        except Exception as e:
                            logger.warning(f"Skipping corrupted image {img_path}: {e}")
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        img_path = self.images[idx]
        try:
            image = Image.open(img_path).convert('RGB')
            label = self.labels[idx]
            
            if self.transform:
                image = self.transform(image)
            
            return image, label
        except Exception as e:
            logger.error(f"Error loading image {img_path}: {e}")
            # Return a black image and the label as fallback
            return torch.zeros(3, 224, 224), self.labels[idx]
    
    @staticmethod
    def get_strong_augmentation():
        """Enhanced augmentation to reduce false positives."""
        return transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.RandomCrop((224, 224)),
            # Color augmentation - helps model be invariant to lighting
            transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.2, hue=0.1),
            # Geometric augmentation
            transforms.RandomRotation(degrees=15),
            transforms.RandomAffine(degrees=0, translate=(0.1, 0.1), scale=(0.9, 1.1)),
            transforms.RandomHorizontalFlip(0.5),
            transforms.RandomVerticalFlip(0.5),
            # Subtle blur to reduce overfitting to texture
            transforms.GaussianBlur(kernel_size=3, sigma=(0.1, 0.5)),
            transforms.ToTensor(),
            # Random erasing - teaches model robustness (must be after ToTensor)
            transforms.RandomErasing(p=0.2, scale=(0.02, 0.15)),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    
    @staticmethod
    def get_val_transform():
        """Lighter augmentation for validation."""
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])


class UlcerDetectionModel(nn.Module):
    """Production-ready CNN model with dropout regularization."""
    
    def __init__(self, num_classes=2, pretrained=True, dropout_rate=0.5):
        super(UlcerDetectionModel, self).__init__()
        
        self.resnet = models.resnet50(pretrained=pretrained)
        
        # Remove original FC layer
        num_ftrs = self.resnet.fc.in_features
        
        # Add dropout layer before classification
        self.dropout = nn.Dropout(p=dropout_rate)
        self.fc = nn.Linear(num_ftrs, num_classes)
        
        self.resnet.fc = nn.Identity()  # Remove original FC from resnet
    
    def forward(self, x):
        try:
            features = self.resnet(x)
            features = self.dropout(features)
            output = self.fc(features)
            return output
        except Exception as e:
            logger.error(f"Error in model forward: {e}")
            logger.error(f"Input shape: {x.shape if hasattr(x, 'shape') else 'N/A'}")
            raise e


def compute_class_weights(labels):
    """Compute weights for imbalanced classes."""
    unique, counts = np.unique(labels, return_counts=True)
    total = len(labels)
    weights = {}
    for cls, count in zip(unique, counts):
        weights[cls] = total / (len(unique) * count)
    
    # Normalize to sum to num_classes
    weight_sum = sum(weights.values())
    weights = {k: v * len(weights) / weight_sum for k, v in weights.items()}
    
    logger.info(f"Class weights: {weights}")
    return torch.tensor([weights[i] for i in range(len(weights))], dtype=torch.float32)


def create_stratified_dataloaders(dataset_path, batch_size=32):
    """Create train/val/test splits with stratification."""
    
    # Load all images with labels
    full_dataset = UlcerDatasetProduction(dataset_path, transform=None)
    labels = np.array(full_dataset.labels)
    
    logger.info(f"Total samples: {len(labels)}")
    logger.info(f"Normal: {(labels == 0).sum()}, Ulcers: {(labels == 1).sum()}")
    
    # First split: 80% train+val, 20% test
    splitter1 = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    train_val_idx, test_idx = next(splitter1.split(range(len(labels)), labels))
    
    # Second split: 75% train, 25% val (from train_val)
    train_val_labels = labels[train_val_idx]
    splitter2 = StratifiedShuffleSplit(n_splits=1, test_size=0.25, random_state=42)
    train_idx, val_idx = next(splitter2.split(range(len(train_val_idx)), train_val_labels))
    
    # Map back to original indices
    train_idx = train_val_idx[train_idx]
    val_idx = train_val_idx[val_idx]
    
    logger.info(f"Train: {len(train_idx)}, Val: {len(val_idx)}, Test: {len(test_idx)}")
    
    # Create datasets with proper transforms
    train_dataset = UlcerDatasetProduction(
        dataset_path,
        indices=train_idx,
        transform=UlcerDatasetProduction.get_strong_augmentation()
    )
    
    val_dataset = UlcerDatasetProduction(
        dataset_path,
        indices=val_idx,
        transform=UlcerDatasetProduction.get_val_transform()
    )
    
    test_dataset = UlcerDatasetProduction(
        dataset_path,
        indices=test_idx,
        transform=UlcerDatasetProduction.get_val_transform()
    )
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=2)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=2)
    
    return train_loader, val_loader, test_loader, labels[train_idx]


def train_epoch(model, train_loader, criterion, optimizer, device, class_weights):
    """Train for one epoch."""
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    for images, labels in train_loader:
        try:
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            
            # Use class weights in loss
            loss = criterion(outputs, labels)
            loss.backward()
            
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            
            total_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        except Exception as e:
            logger.error(f"Error in training batch: {e}")
            logger.error(f"Image shape: {images.shape if 'images' in locals() else 'N/A'}")
            raise e
    
    return total_loss / len(train_loader), correct / total


def validate(model, val_loader, criterion, device):
    """Validate model."""
    model.eval()
    total_loss = 0
    correct = 0
    total = 0
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            total_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    # Compute per-class accuracy
    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)
    
    normal_acc = (all_preds[all_labels == 0] == 0).sum() / (all_labels == 0).sum() if (all_labels == 0).sum() > 0 else 0
    ulcer_acc = (all_preds[all_labels == 1] == 1).sum() / (all_labels == 1).sum() if (all_labels == 1).sum() > 0 else 0
    
    return total_loss / len(val_loader), correct / total, normal_acc, ulcer_acc


def train_model(dataset_path, num_epochs=100, batch_size=32, learning_rate=0.001, output_dir="./models"):
    """Main training loop with early stopping."""
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")
    
    # Create dataloaders
    train_loader, val_loader, test_loader, train_labels = create_stratified_dataloaders(
        dataset_path, batch_size=batch_size
    )
    
    # Initialize model
    model = UlcerDetectionModel(num_classes=2, pretrained=True, dropout_rate=0.5)
    model = model.to(device)
    
    # Class weights for imbalanced dataset
    class_weights = compute_class_weights(train_labels)
    class_weights = class_weights.to(device)
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    optimizer = optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=5, min_lr=1e-7
    )
    
    # Training history
    history = {
        'train_loss': [],
        'train_acc': [],
        'val_loss': [],
        'val_acc': [],
        'val_normal_acc': [],
        'val_ulcer_acc': [],
        'learning_rate': []
    }
    
    best_val_loss = float('inf')
    patience = 15
    patience_counter = 0
    
    for epoch in range(num_epochs):
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device, class_weights)
        val_loss, val_acc, normal_acc, ulcer_acc = validate(model, val_loader, criterion, device)
        
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)
        history['val_normal_acc'].append(normal_acc)
        history['val_ulcer_acc'].append(ulcer_acc)
        history['learning_rate'].append(optimizer.param_groups[0]['lr'])
        
        logger.info(
            f"Epoch {epoch+1}/{num_epochs} | "
            f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f} | "
            f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.4f} | "
            f"Normal Acc: {normal_acc:.4f} | Ulcer Acc: {ulcer_acc:.4f}"
        )
        
        # Learning rate scheduling
        scheduler.step(val_loss)
        
        # Early stopping and best model saving
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            
            best_model_path = os.path.join(output_dir, 'ulcer_detection_model_best.pth')
            torch.save({
                'model_state_dict': model.state_dict(),
                'epoch': epoch,
                'val_loss': val_loss,
                'val_acc': val_acc
            }, best_model_path)
            logger.info(f"Best model saved: {best_model_path}")
        else:
            patience_counter += 1
            if patience_counter >= patience:
                logger.info(f"Early stopping at epoch {epoch+1}")
                break
    
    # Test on unseen test data
    logger.info("\n" + "="*50)
    logger.info("TESTING ON UNSEEN DATA")
    logger.info("="*50)
    
    model.load_state_dict(torch.load(best_model_path)['model_state_dict'])
    test_loss, test_acc, test_normal_acc, test_ulcer_acc = validate(model, test_loader, criterion, device)
    
    logger.info(f"Test Loss: {test_loss:.4f}")
    logger.info(f"Test Accuracy: {test_acc:.4f}")
    logger.info(f"Normal Accuracy: {test_normal_acc:.4f}")
    logger.info(f"Ulcer Accuracy: {test_ulcer_acc:.4f}")
    
    # Save final model
    final_model_path = os.path.join(output_dir, 'ulcer_detection_model_production.pth')
    torch.save({
        'model_state_dict': model.state_dict(),
        'test_accuracy': test_acc,
        'test_normal_accuracy': test_normal_acc,
        'test_ulcer_accuracy': test_ulcer_acc
    }, final_model_path)
    
    # Save history
    history_path = os.path.join(output_dir, 'training_history.json')
    with open(history_path, 'w') as f:
        json.dump(history, f, indent=2)
    
    logger.info(f"\nFinal model saved: {final_model_path}")
    logger.info(f"Training history saved: {history_path}")
    
    return model, history


if __name__ == "__main__":
    import os
    # Get project root dynamically
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    dataset_path = os.path.join(project_root, "datasets", "images")
    output_dir = os.path.join(project_root, "model_weights")
    
    logger.info("Starting production-level model training...")
    logger.info(f"Dataset path: {dataset_path}")
    logger.info(f"Output directory: {output_dir}")
    
    model, history = train_model(
        dataset_path=dataset_path,
        num_epochs=100,
        batch_size=16,  # Reduced from 32 to 16 for stability
        learning_rate=0.001,
        output_dir=output_dir
    )
    
    logger.info("Training complete!")
