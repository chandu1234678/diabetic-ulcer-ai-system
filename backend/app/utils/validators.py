"""Validation utilities."""

import logging
from typing import Tuple, List
from PIL import Image
import re

logger = logging.getLogger(__name__)


class InputValidator:
    """Validated input data."""
    
    ALLOWED_IMAGE_FORMATS = {".jpg", ".jpeg", ".png", ".tiff", ".tif"}
    MIN_IMAGE_SIZE = 100
    MAX_IMAGE_SIZE = 4096
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @staticmethod
    def validate_patient_id(patient_id: str) -> Tuple[bool, str]:
        """
        Validate patient ID format.
        
        Args:
            patient_id: Patient ID string
        
        Returns:
            Tuple of (is_valid, message)
        """
        if not patient_id:
            return False, "Patient ID cannot be empty"
        
        if len(patient_id) > 50:
            return False, "Patient ID too long"
        
        # Allow alphanumeric and common separators
        if not re.match(r"^[a-zA-Z0-9\-_]*$", patient_id):
            return False, "Invalid patient ID format"
        
        return True, "Valid"
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Validate email format."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        
        if re.match(pattern, email):
            return True, "Valid"
        else:
            return False, "Invalid email format"
    
    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        """Validate phone number format."""
        # Accept various phone formats
        pattern = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
        
        if re.match(pattern, phone.replace(" ", "")):
            return True, "Valid"
        else:
            return False, "Invalid phone format"
    
    @staticmethod
    def validate_image_file(
        filename: str,
        file_size: int
    ) -> Tuple[bool, str]:
        """
        Validate image file.
        
        Args:
            filename: Image filename
            file_size: File size in bytes
        
        Returns:
            Tuple of (is_valid, message)
        """
        # Check extension
        ext = "." + filename.split(".")[-1].lower()
        if ext not in InputValidator.ALLOWED_IMAGE_FORMATS:
            return False, f"Invalid format. Allowed: {InputValidator.ALLOWED_IMAGE_FORMATS}"
        
        # Check file size
        if file_size > InputValidator.MAX_FILE_SIZE:
            return False, f"File too large. Max: {InputValidator.MAX_FILE_SIZE / 1024 / 1024}MB"
        
        return True, "Valid"
    
    @staticmethod
    def validate_image_dimensions(
        image: Image.Image
    ) -> Tuple[bool, str]:
        """
        Validate image dimensions.
        
        Args:
            image: PIL Image
        
        Returns:
            Tuple of (is_valid, message)
        """
        width, height = image.size
        
        if width < InputValidator.MIN_IMAGE_SIZE or height < InputValidator.MIN_IMAGE_SIZE:
            return False, f"Image too small. Min: {InputValidator.MIN_IMAGE_SIZE}x{InputValidator.MIN_IMAGE_SIZE}"
        
        if width > InputValidator.MAX_IMAGE_SIZE or height > InputValidator.MAX_IMAGE_SIZE:
            return False, f"Image too large. Max: {InputValidator.MAX_IMAGE_SIZE}x{InputValidator.MAX_IMAGE_SIZE}"
        
        # Check aspect ratio
        aspect_ratio = max(width, height) / min(width, height)
        if aspect_ratio > 3:
            return False, "Invalid aspect ratio (too extreme)"
        
        return True, "Valid"
    
    @staticmethod
    def validate_confidence_score(score: float) -> Tuple[bool, str]:
        """Validate confidence score."""
        if score < 0 or score > 1:
            return False, "Confidence score must be between 0 and 1"
        return True, "Valid"
    
    @staticmethod
    def validate_numeric_range(
        value: float,
        min_val: float,
        max_val: float,
        field_name: str
    ) -> Tuple[bool, str]:
        """
        Validate numeric range.
        
        Args:
            value: Value to validate
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            field_name: Field name for error message
        
        Returns:
            Tuple of (is_valid, message)
        """
        if value < min_val or value > max_val:
            return False, f"{field_name} must be between {min_val} and {max_val}"
        return True, "Valid"
    
    @staticmethod
    def validate_required_fields(
        data: dict,
        required_fields: List[str]
    ) -> Tuple[bool, str]:
        """
        Validate required fields.
        
        Args:
            data: Data dictionary
            required_fields: List of required field names
        
        Returns:
            Tuple of (is_valid, message)
        """
        missing = [field for field in required_fields if field not in data or data[field] is None]
        
        if missing:
            return False, f"Missing required fields: {', '.join(missing)}"
        
        return True, "Valid"


class ModelOutputValidator:
    """Validate model outputs."""
    
    @staticmethod
    def validate_prediction_output(output: dict) -> Tuple[bool, str]:
        """
        Validate prediction output.
        
        Args:
            output: Prediction dictionary
        
        Returns:
            Tuple of (is_valid, message)
        """
        required_keys = {"predicted_class", "confidence"}
        
        if not all(key in output for key in required_keys):
            return False, f"Missing required keys: {required_keys}"
        
        # Validate confidence
        if not isinstance(output["confidence"], (int, float)):
            return False, "Confidence must be numeric"
        
        if output["confidence"] < 0 or output["confidence"] > 1:
            return False, "Confidence must be between 0 and 1"
        
        return True, "Valid"
    
    @staticmethod
    def validate_segmentation_output(
        mask: object,
        expected_shape: Tuple
    ) -> Tuple[bool, str]:
        """
        Validate segmentation output.
        
        Args:
            mask: Segmentation mask
            expected_shape: Expected shape
        
        Returns:
            Tuple of (is_valid, message)
        """
        if mask.shape != expected_shape:
            return False, f"Shape mismatch. Expected {expected_shape}, got {mask.shape}"
        
        # Check value range
        if mask.min() < 0 or mask.max() > 1:
            return False, "Mask values must be between 0 and 1"
        
        return True, "Valid"


def validate_input(data: dict, schema: type) -> Tuple[bool, str]:
    """Validate input against schema."""
    try:
        schema(**data)
        return True, "Valid"
    except Exception as e:
        return False, str(e)
