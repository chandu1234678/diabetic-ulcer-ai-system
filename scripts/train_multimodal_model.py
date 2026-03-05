"""
Train multimodal model combining image and clinical data
"""

import argparse
import logging
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import matplotlib.pyplot as plt
import numpy as np

logger = logging.getLogger(__name__)


class MultimodalDataset(Dataset):
    """Dataset for multimodal learning with image + clinical data"""
    
    def __init__(self, image_dir: str, clinical_data_file: str, transform=None):
        self.image_dir = Path(image_dir)
        self.clinical_data_file = clinical_data_file
        self.transform = transform
        self.images = list(self.image_dir.glob("*.jpg")) + list(self.image_dir.glob("*.png"))
        
        # Load clinical data
        self.clinical_data = self._load_clinical_data()
    
    def _load_clinical_data(self):
        # Placeholder for loading clinical data
        # In real scenario, load from CSV
        return {}
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        # Placeholder implementation
        image = torch.randn(3, 256, 256)
        clinical = torch.randn(10)  # 10 clinical features
        label = torch.tensor([0], dtype=torch.float32)
        return image, clinical, label


class MultimodalModel(nn.Module):
    """Multimodal fusion network"""
    
    def __init__(self, num_clinical_features: int = 10, num_classes: int = 1):
        super().__init__()
        
        # Image branch - CNN
        self.image_branch = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten()
        )
        
        # Clinical branch - MLP
        self.clinical_branch = nn.Sequential(
            nn.Linear(num_clinical_features, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.BatchNorm1d(32)
        )
        
        # Fusion layer
        self.fusion = nn.Sequential(
            nn.Linear(128 + 32, 128),
            nn.ReLU(),
            nn.BatchNorm1d(128),
            nn.Dropout(0.5),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Dropout(0.5),
            nn.Linear(64, num_classes)
        )
    
    def forward(self, image, clinical):
        # Process image
        image_features = self.image_branch(image)
        
        # Process clinical data
        clinical_features = self.clinical_branch(clinical)
        
        # Fusion
        fused = torch.cat([image_features, clinical_features], dim=1)
        output = self.fusion(fused)
        output = torch.sigmoid(output)
        
        return output, image_features, clinical_features


def train_multimodal_model(
    image_dir: str,
    clinical_data_file: str,
    output_dir: str = "model_weights",
    epochs: int = 50,
    batch_size: int = 16,
    learning_rate: float = 1e-4,
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
):
    """
    Train the multimodal model
    
    Args:
        image_dir: Directory containing training images
        clinical_data_file: Path to clinical data file
        output_dir: Directory to save model weights
        epochs: Number of training epochs
        batch_size: Batch size for training
        learning_rate: Learning rate
        device: Device to train on
    """
    
    logger.info("Starting multimodal model training...")
    logger.info(f"Device: {device}")
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Initialize dataset and dataloader
    dataset = MultimodalDataset(image_dir, clinical_data_file)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    # Initialize model
    model = MultimodalModel(num_clinical_features=10, num_classes=1)
    model = model.to(device)
    
    # Loss and optimizer
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.5)
    
    # Training loop
    train_losses = []
    
    for epoch in range(epochs):
        model.train()
        epoch_loss = 0
        
        for batch_idx, (images, clinical, labels) in enumerate(dataloader):
            images, clinical, labels = (
                images.to(device),
                clinical.to(device),
                labels.to(device)
            )
            
            optimizer.zero_grad()
            outputs, _, _ = model(images, clinical)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            epoch_loss += loss.item()
        
        avg_loss = epoch_loss / len(dataloader)
        train_losses.append(avg_loss)
        
        logger.info(f"Epoch {epoch+1}/{epochs} - Loss: {avg_loss:.4f}")
        
        scheduler.step()
        
        # Save checkpoint every 10 epochs
        if (epoch + 1) % 10 == 0:
            checkpoint_path = Path(output_dir) / f"multimodal_model_epoch_{epoch+1}.pth"
            torch.save(model.state_dict(), checkpoint_path)
            logger.info(f"Checkpoint saved: {checkpoint_path}")
    
    # Save final model
    final_path = Path(output_dir) / "multimodal_model.pth"
    torch.save(model.state_dict(), final_path)
    logger.info(f"Final model saved: {final_path}")
    
    # Plot loss curve
    plt.figure(figsize=(10, 6))
    plt.plot(train_losses, label='Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Multimodal Model Training Loss')
    plt.legend()
    plt.grid(True)
    plt.savefig(Path(output_dir) / "multimodal_training_loss.png")
    logger.info("Loss plot saved")
    
    return model


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train multimodal model")
    parser.add_argument("--image-dir", type=str, default="datasets/images/ulcers",
                        help="Path to training images")
    parser.add_argument("--clinical-data", type=str, default="datasets/clinical_data/patient_data.csv",
                        help="Path to clinical data CSV")
    parser.add_argument("--output-dir", type=str, default="model_weights",
                        help="Path to save model weights")
    parser.add_argument("--epochs", type=int, default=50,
                        help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=16,
                        help="Batch size")
    parser.add_argument("--learning-rate", type=float, default=1e-4,
                        help="Learning rate")
    
    args = parser.parse_args()
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )
    
    train_multimodal_model(
        image_dir=args.image_dir,
        clinical_data_file=args.clinical_data,
        output_dir=args.output_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate
    )
