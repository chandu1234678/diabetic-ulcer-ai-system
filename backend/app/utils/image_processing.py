"""Image processing utilities."""

import numpy as np
from PIL import Image, ImageOps, ImageEnhance
import logging
from typing import Tuple, Optional
import cv2

logger = logging.getLogger(__name__)


class ImageProcessor:
    """Utility class for image processing."""
    
    @staticmethod
    def normalize_image(image: Image.Image) -> Image.Image:
        """
        Normalize image to standard format.
        
        Args:
            image: PIL Image
        
        Returns:
            Normalized image
        """
        try:
            # Convert to RGB
            if image.mode != "RGB":
                image = image.convert("RGB")
            
            # Normalize size
            image.thumbnail((512, 512), Image.Resampling.LANCZOS)
            
            logger.debug("Normalized image")
            return image
        except Exception as e:
            logger.error(f"Error normalizing image: {str(e)}")
            raise
    
    @staticmethod
    def apply_clahe(image_array: np.ndarray, clip_limit: float = 2.0) -> np.ndarray:
        """
        Apply Contrast Limited Adaptive Histogram Equalization.
        
        Args:
            image_array: Image as numpy array
            clip_limit: CLAHE clip limit
        
        Returns:
            Enhanced image array
        """
        try:
            # Convert to HSV for better processing
            if len(image_array.shape) == 3:
                hsv = cv2.cvtColor(image_array, cv2.COLOR_RGB2HSV)
                v = hsv[:, :, 2]
            else:
                v = image_array
            
            # Apply CLAHE
            clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
            enhanced_v = clahe.apply(v)
            
            # Reconstruct if HSV
            if len(image_array.shape) == 3:
                hsv[:, :, 2] = enhanced_v
                enhanced = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
            else:
                enhanced = enhanced_v
            
            logger.debug("Applied CLAHE enhancement")
            return enhanced
        except Exception as e:
            logger.error(f"Error applying CLAHE: {str(e)}")
            return image_array
    
    @staticmethod
    def apply_gaussian_blur(image_array: np.ndarray, kernel_size: int = 5) -> np.ndarray:
        """
        Apply Gaussian blur for noise reduction.
        
        Args:
            image_array: Image as numpy array
            kernel_size: Kernel size (must be odd)
        
        Returns:
            Blurred image array
        """
        try:
            if kernel_size % 2 == 0:
                kernel_size += 1
            
            blurred = cv2.GaussianBlur(image_array, (kernel_size, kernel_size), 0)
            logger.debug("Applied Gaussian blur")
            return blurred
        except Exception as e:
            logger.error(f"Error applying Gaussian blur: {str(e)}")
            return image_array
    
    @staticmethod
    def apply_bilateral_filter(
        image_array: np.ndarray,
        diameter: int = 9,
        sigma_color: float = 75,
        sigma_space: float = 75
    ) -> np.ndarray:
        """
        Apply bilateral filter for edge-preserving smoothing.
        
        Args:
            image_array: Image as numpy array
            diameter: Kernel diameter
            sigma_color: Color space sigma
            sigma_space: Coordinate space sigma
        
        Returns:
            Filtered image array
        """
        try:
            filtered = cv2.bilateralFilter(
                image_array, diameter, sigma_color, sigma_space
            )
            logger.debug("Applied bilateral filter")
            return filtered
        except Exception as e:
            logger.error(f"Error applying bilateral filter: {str(e)}")
            return image_array
    
    @staticmethod
    def enhance_contrast(image: Image.Image, factor: float = 1.5) -> Image.Image:
        """
        Enhance image contrast.
        
        Args:
            image: PIL Image
            factor: Enhancement factor (> 1 increases contrast)
        
        Returns:
            Enhanced image
        """
        try:
            enhancer = ImageEnhance.Contrast(image)
            enhanced = enhancer.enhance(factor)
            logger.debug(f"Enhanced contrast by factor {factor}")
            return enhanced
        except Exception as e:
            logger.error(f"Error enhancing contrast: {str(e)}")
            return image
    
    @staticmethod
    def enhance_brightness(image: Image.Image, factor: float = 1.1) -> Image.Image:
        """
        Enhance image brightness.
        
        Args:
            image: PIL Image
            factor: Enhancement factor
        
        Returns:
            Enhanced image
        """
        try:
            enhancer = ImageEnhance.Brightness(image)
            enhanced = enhancer.enhance(factor)
            logger.debug(f"Enhanced brightness by factor {factor}")
            return enhanced
        except Exception as e:
            logger.error(f"Error enhancing brightness: {str(e)}")
            return image
    
    @staticmethod
    def equalize_histogram(image_array: np.ndarray) -> np.ndarray:
        """
        Equalize image histogram.
        
        Args:
            image_array: Image as numpy array
        
        Returns:
            Equalized image array
        """
        try:
            if len(image_array.shape) == 3:
                # Apply to each channel
                equalized = np.stack([
                    cv2.equalizeHist(image_array[:, :, i])
                    for i in range(3)
                ], axis=2)
            else:
                equalized = cv2.equalizeHist(image_array)
            
            logger.debug("Applied histogram equalization")
            return equalized
        except Exception as e:
            logger.error(f"Error equalizing histogram: {str(e)}")
            return image_array
    
    @staticmethod
    def detect_edges(image_array: np.ndarray, method: str = "canny") -> np.ndarray:
        """
        Detect edges in image.
        
        Args:
            image_array: Image as numpy array
            method: Detection method ("canny" or "sobel")
        
        Returns:
            Edge mask
        """
        try:
            # Convert to grayscale if needed
            if len(image_array.shape) == 3:
                gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = image_array
            
            if method == "canny":
                edges = cv2.Canny(gray, 100, 200)
            elif method == "sobel":
                sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
                sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
                edges = np.sqrt(sobelx ** 2 + sobely ** 2).astype(np.uint8)
            else:
                edges = cv2.Canny(gray, 100, 200)
            
            logger.debug(f"Detected edges using {method}")
            return edges
        except Exception as e:
            logger.error(f"Error detecting edges: {str(e)}")
            return image_array
    
    @staticmethod
    def rotate_image(image: Image.Image, angle: float) -> Image.Image:
        """
        Rotate image.
        
        Args:
            image: PIL Image
            angle: Rotation angle in degrees
        
        Returns:
            Rotated image
        """
        try:
            rotated = image.rotate(angle, expand=True)
            logger.debug(f"Rotated image by {angle} degrees")
            return rotated
        except Exception as e:
            logger.error(f"Error rotating image: {str(e)}")
            return image
    
    @staticmethod
    def crop_to_content(image_array: np.ndarray) -> Tuple[np.ndarray, Tuple]:
        """
        Crop image to content (remove black borders).
        
        Args:
            image_array: Image as numpy array
        
        Returns:
            Cropped image and crop coordinates
        """
        try:
            if len(image_array.shape) == 3:
                gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = image_array
            
            _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
                cropped = image_array[y:y+h, x:x+w]
                logger.debug(f"Cropped image to content")
                return cropped, (x, y, w, h)
            
            return image_array, (0, 0, image_array.shape[1], image_array.shape[0])
        except Exception as e:
            logger.error(f"Error cropping image: {str(e)}")
            return image_array, None


def create_image_processor() -> ImageProcessor:
    """Create image processor utility."""
    return ImageProcessor()
