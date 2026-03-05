"""Image preprocessing pipeline."""

import numpy as np
from PIL import Image
from typing import Tuple
import torch
import torchvision.transforms as transforms
import logging

logger = logging.getLogger(__name__)


class PreprocessingPipeline:
    """
    Image preprocessing pipeline for model input preparation.
    
    Operations:
    - Image normalization
    - Resizing
    - Tensor conversion
    - Augmentation (optional)
    """
    
    def __init__(
        self,
        image_size: int = 224,
        mean: Tuple[float, ...] = (0.485, 0.456, 0.406),
        std: Tuple[float, ...] = (0.229, 0.224, 0.225)
    ):
        """
        Initialize preprocessing pipeline.
        
        Args:
            image_size: Target image size
            mean: Normalization mean
            std: Normalization std
        """
        self.image_size = image_size
        self.mean = mean
        self.std = std
        
        self.transform = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=mean, std=std)
        ])
        
        self.transform_with_aug = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.RandomRotation(10),
            transforms.RandomHorizontalFlip(),
            transforms.ColorJitter(
                brightness=0.1,
                contrast=0.1,
                saturation=0.1
            ),
            transforms.ToTensor(),
            transforms.Normalize(mean=mean, std=std)
        ])
    
    def preprocess(
        self,
        image: Image.Image,
        augment: bool = False
    ) -> torch.Tensor:
        """
        Preprocess a single image.
        
        Args:
            image: PIL Image
            augment: Whether to apply augmentation
        
        Returns:
            Preprocessed tensor
        """
        try:
            # Convert to RGB if needed
            if image.mode != "RGB":
                image = image.convert("RGB")
            
            # Apply transforms
            transform = self.transform_with_aug if augment else self.transform
            tensor = transform(image)
            
            logger.debug(f"Preprocessed image to shape {tensor.shape}")
            return tensor
        
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            raise
    
    def preprocess_batch(
        self,
        images: list,
        augment: bool = False
    ) -> torch.Tensor:
        """
        Preprocess a batch of images.
        
        Args:
            images: List of PIL Images
            augment: Whether to apply augmentation
        
        Returns:
            Batch tensor of shape (B, C, H, W)
        """
        tensors = [self.preprocess(img, augment) for img in images]
        return torch.stack(tensors)
    
    def postprocess_mask(
        self,
        mask: np.ndarray,
        original_size: Tuple[int, int]
    ) -> np.ndarray:
        """
        Postprocess segmentation mask.
        
        Args:
            mask: Predicted mask
            original_size: Original image size
        
        Returns:
            Resized mask
        """
        try:
            # Convert to PIL and resize
            mask_pil = Image.fromarray((mask * 255).astype(np.uint8))
            mask_resized = mask_pil.resize(original_size)
            
            return np.array(mask_resized) / 255.0
        
        except Exception as e:
            logger.error(f"Error postprocessing mask: {str(e)}")
            raise


def create_preprocessing_pipeline(
    image_size: int = 224,
    **kwargs
) -> PreprocessingPipeline:
    """
    Create preprocessing pipeline.
    
    Args:
        image_size: Target image size
        **kwargs: Additional arguments
    
    Returns:
        Initialized pipeline
    """
    return PreprocessingPipeline(image_size=image_size, **kwargs)
