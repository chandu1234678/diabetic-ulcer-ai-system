"""CNN-based ulcer classification model."""

import torch
import torch.nn as nn
from torchvision import models
import logging

logger = logging.getLogger(__name__)


class CNNUlcerModel(nn.Module):
    """
    CNN model for ulcer detection and classification.
    
    Architecture: ResNet50 backbone with custom classification head
    """
    
    def __init__(self, num_classes: int = 3, pretrained: bool = True):
        """
        Initialize CNN model.
        
        Args:
            num_classes: Number of output classes (default: 3 - normal, ulcer, severe)
            pretrained: Whether to use pretrained weights
        """
        super(CNNUlcerModel, self).__init__()
        
        self.backbone = models.resnet50(pretrained=pretrained)
        
        # Remove the original classification head
        num_features = self.backbone.fc.in_features
        
        # Custom classification head
        self.backbone.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(num_features, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
            nn.Linear(256, num_classes)
        )
        
        self.num_classes = num_classes
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass.
        
        Args:
            x: Input tensor of shape (B, 3, H, W)
        
        Returns:
            Logits of shape (B, num_classes)
        """
        return self.backbone(x)
    
    def get_feature_maps(self, x: torch.Tensor) -> torch.Tensor:
        """
        Extract feature maps from the backbone.
        
        Args:
            x: Input tensor
        
        Returns:
            Feature maps
        """
        return self.backbone.layer4(self.backbone.layer3(
            self.backbone.layer2(self.backbone.layer1(
                self.backbone.conv1(x)
            ))
        ))


def create_cnn_model(num_classes: int = 3, pretrained: bool = True) -> CNNUlcerModel:
    """
    Create and return a CNN ulcer model.
    
    Args:
        num_classes: Number of classification classes
        pretrained: Whether to use pretrained weights
    
    Returns:
        Initialized CNNUlcerModel
    """
    model = CNNUlcerModel(num_classes=num_classes, pretrained=pretrained)
    logger.info(f"Created CNN model with {num_classes} classes")
    return model
