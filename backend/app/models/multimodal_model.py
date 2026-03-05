"""Multimodal model combining image and clinical data."""

import torch
import torch.nn as nn
from typing import Tuple, Dict
import logging

logger = logging.getLogger(__name__)


class MultimodalModel(nn.Module):
    """
    Multimodal model that combines image features with clinical data.
    
    Architecture:
    - Image branch: CNN feature extractor
    - Clinical branch: Dense network on clinical data
    - Fusion: Concatenation followed by dense layers
    """
    
    def __init__(
        self,
        image_feature_dim: int = 2048,
        clinical_feature_dim: int = 10,
        hidden_dim: int = 512,
        num_classes: int = 3
    ):
        """
        Initialize multimodal model.
        
        Args:
            image_feature_dim: Dimension of image features
            clinical_feature_dim: Number of clinical features
            hidden_dim: Hidden dimension for fusion layers
            num_classes: Number of output classes
        """
        super(MultimodalModel, self).__init__()
        
        # Image feature projection
        self.image_projection = nn.Sequential(
            nn.Linear(image_feature_dim, hidden_dim),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3)
        )
        
        # Clinical features processing
        self.clinical_processor = nn.Sequential(
            nn.Linear(clinical_feature_dim, hidden_dim // 2),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim // 2, hidden_dim // 4)
        )
        
        # Fusion layers
        fusion_input_dim = hidden_dim + hidden_dim // 4
        self.fusion = nn.Sequential(
            nn.Linear(fusion_input_dim, hidden_dim),
            nn.ReLU(inplace=True),
            nn.Dropout(0.4),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim // 2, num_classes)
        )
        
        self.num_classes = num_classes
    
    def forward(
        self,
        image_features: torch.Tensor,
        clinical_data: torch.Tensor
    ) -> torch.Tensor:
        """
        Forward pass.
        
        Args:
            image_features: Image features of shape (B, image_feature_dim)
            clinical_data: Clinical data of shape (B, clinical_feature_dim)
        
        Returns:
            Logits of shape (B, num_classes)
        """
        # Project image features
        image_proj = self.image_projection(image_features)
        
        # Process clinical data
        clinical_proj = self.clinical_processor(clinical_data)
        
        # Fuse modalities
        fused = torch.cat([image_proj, clinical_proj], dim=1)
        
        # Classification
        logits = self.fusion(fused)
        
        return logits
    
    def forward_with_attention(
        self,
        image_features: torch.Tensor,
        clinical_data: torch.Tensor
    ) -> Tuple[torch.Tensor, Dict]:
        """
        Forward pass with attention weights.
        
        Args:
            image_features: Image features
            clinical_data: Clinical data
        
        Returns:
            Logits and attention weights
        """
        # Get projections
        image_proj = self.image_projection(image_features)
        clinical_proj = self.clinical_processor(clinical_data)
        
        # Calculate attention weights
        image_weight = torch.norm(image_proj, p=2, dim=1, keepdim=True)
        clinical_weight = torch.norm(clinical_proj, p=2, dim=1, keepdim=True)
        
        total_weight = image_weight + clinical_weight
        image_attention = image_weight / (total_weight + 1e-8)
        clinical_attention = clinical_weight / (total_weight + 1e-8)
        
        # Fuse
        fused = torch.cat([image_proj, clinical_proj], dim=1)
        logits = self.fusion(fused)
        
        return logits, {
            "image_weight": image_attention.squeeze(),
            "clinical_weight": clinical_attention.squeeze()
        }


def create_multimodal_model(
    image_feature_dim: int = 2048,
    clinical_feature_dim: int = 10,
    num_classes: int = 3
) -> MultimodalModel:
    """
    Create and return a multimodal model.
    
    Args:
        image_feature_dim: Image feature dimension
        clinical_feature_dim: Clinical feature dimension
        num_classes: Number of classes
    
    Returns:
        Initialized MultimodalModel
    """
    model = MultimodalModel(
        image_feature_dim=image_feature_dim,
        clinical_feature_dim=clinical_feature_dim,
        num_classes=num_classes
    )
    logger.info("Created multimodal model")
    return model
