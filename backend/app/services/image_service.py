"""Image processing and management service."""

import logging
from pathlib import Path
from typing import Optional, List, Tuple
from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)

SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".tiff", ".tif"}


class ImageService:
    """
    Service for image processing and validation.
    
    Features:
    - Image validation
    - Quality assessment
    - Format conversion
    - Storage management
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize image service.
        
        Args:
            storage_path: Path to image storage directory
        """
        self.storage_path = Path(storage_path) if storage_path else None
        if self.storage_path:
            self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def validate_image(self, image: Image.Image) -> Tuple[bool, str]:
        """
        Validate image for processing.
        
        Args:
            image: PIL Image
        
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            # Check format
            if image.format and image.format.lower() not in SUPPORTED_FORMATS:
                return False, f"Unsupported format: {image.format}"
            
            # Check dimensions
            width, height = image.size
            if width < 100 or height < 100:
                return False, "Image too small (min 100x100)"
            
            if width > 4096 or height > 4096:
                return False, "Image too large (max 4096x4096)"
            
            # Check aspect ratio
            aspect_ratio = width / height
            if aspect_ratio < 0.5 or aspect_ratio > 2:
                return False, "Invalid aspect ratio"
            
            logger.info(f"Valid image: {width}x{height}")
            return True, "Valid"
        
        except Exception as e:
            logger.error(f"Error validating image: {str(e)}")
            return False, f"Validation error: {str(e)}"
    
    def assess_image_quality(self, image: Image.Image) -> dict:
        """
        Assess image quality metrics.
        
        Args:
            image: PIL Image
        
        Returns:
            Quality metrics dictionary
        """
        try:
            img_array = np.array(image)
            
            # Convert to grayscale if needed
            if len(img_array.shape) == 3:
                gray = np.dot(img_array[..., :3], [0.2989, 0.5870, 0.1140])
            else:
                gray = img_array
            
            # Compute metrics
            contrast = np.std(gray)
            brightness = np.mean(gray)
            sharpness = np.std(np.gradient(gray))
            
            metrics = {
                "brightness": float(brightness),
                "contrast": float(contrast),
                "sharpness": float(sharpness),
                "dimensions": image.size,
                "mode": image.mode,
                "quality_score": self._calculate_quality_score(
                    brightness, contrast, sharpness
                )
            }
            
            logger.debug(f"Quality metrics: {metrics}")
            return metrics
        
        except Exception as e:
            logger.error(f"Error assessing quality: {str(e)}")
            return {"error": str(e)}
    
    def _calculate_quality_score(
        self,
        brightness: float,
        contrast: float,
        sharpness: float
    ) -> float:
        """Calculate overall quality score (0-1)."""
        # Normalize metrics
        brightness_score = min(brightness / 255, 1.0)
        contrast_score = min(contrast / 100, 1.0)
        sharpness_score = min(sharpness / 50, 1.0)
        
        # Weighted average
        quality = (
            0.3 * brightness_score +
            0.35 * contrast_score +
            0.35 * sharpness_score
        )
        
        return min(max(quality, 0), 1.0)
    
    def resize_image(
        self,
        image: Image.Image,
        size: Tuple[int, int]
    ) -> Image.Image:
        """
        Resize image maintaining aspect ratio.
        
        Args:
            image: PIL Image
            size: Target size (width, height)
        
        Returns:
            Resized image
        """
        try:
            image.thumbnail(size, Image.Resampling.LANCZOS)
            logger.debug(f"Resized image to {image.size}")
            return image
        except Exception as e:
            logger.error(f"Error resizing image: {str(e)}")
            raise
    
    def save_image(
        self,
        image: Image.Image,
        filename: str,
        quality: int = 95
    ) -> Optional[Path]:
        """
        Save image to storage.
        
        Args:
            image: PIL Image
            filename: Output filename
            quality: JPEG quality (0-100)
        
        Returns:
            Path to saved image or None
        """
        try:
            if not self.storage_path:
                logger.warning("No storage path configured")
                return None
            
            filepath = self.storage_path / filename
            
            # Convert format if needed
            if filepath.suffix.lower() == ".jpg" or filepath.suffix.lower() == ".jpeg":
                if image.mode == "RGBA":
                    image = image.convert("RGB")
                image.save(filepath, quality=quality)
            else:
                image.save(filepath)
            
            logger.info(f"Saved image to {filepath}")
            return filepath
        
        except Exception as e:
            logger.error(f"Error saving image: {str(e)}")
            return None
    
    def load_image(self, filepath: Path) -> Optional[Image.Image]:
        """
        Load image from file.
        
        Args:
            filepath: Path to image file
        
        Returns:
            PIL Image or None
        """
        try:
            image = Image.open(filepath)
            logger.debug(f"Loaded image from {filepath}")
            return image
        except Exception as e:
            logger.error(f"Error loading image: {str(e)}")
            return None
    
    def get_image_statistics(self, image: Image.Image) -> dict:
        """Get image statistics."""
        try:
            img_array = np.array(image)
            
            if len(img_array.shape) == 3:
                stats = {
                    "width": int(img_array.shape[1]),
                    "height": int(img_array.shape[0]),
                    "channels": int(img_array.shape[2]),
                    "dtype": str(img_array.dtype),
                    "mean": float(img_array.mean()),
                    "std": float(img_array.std()),
                    "min": float(img_array.min()),
                    "max": float(img_array.max())
                }
            else:
                stats = {
                    "width": int(img_array.shape[1]),
                    "height": int(img_array.shape[0]),
                    "channels": 1,
                    "dtype": str(img_array.dtype),
                    "mean": float(img_array.mean()),
                    "std": float(img_array.std()),
                    "min": float(img_array.min()),
                    "max": float(img_array.max())
                }
            
            return stats
        
        except Exception as e:
            logger.error(f"Error computing statistics: {str(e)}")
            return {}


def create_image_service(storage_path: Optional[str] = None) -> ImageService:
    """Create image service."""
    return ImageService(storage_path)
