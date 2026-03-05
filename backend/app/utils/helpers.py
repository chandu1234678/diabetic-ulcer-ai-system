"""Helper utilities."""

import logging
import numpy as np
from typing import Any, Dict, List, Optional, Tuple
import json
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)


class DataHelper:
    """Data manipulation helpers."""
    
    @staticmethod
    def dict_to_json(data: dict, indent: int = 2) -> str:
        """Convert dictionary to JSON string."""
        try:
            return json.dumps(data, indent=indent, default=str)
        except Exception as e:
            logger.error(f"Error converting to JSON: {str(e)}")
            return ""
    
    @staticmethod
    def json_to_dict(json_str: str) -> Optional[dict]:
        """Convert JSON string to dictionary."""
        try:
            return json.loads(json_str)
        except Exception as e:
            logger.error(f"Error parsing JSON: {str(e)}")
            return None
    
    @staticmethod
    def flatten_dict(d: dict, parent_key: str = "", sep: str = "_") -> dict:
        """Flatten nested dictionary."""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(
                    DataHelper.flatten_dict(v, new_key, sep=sep).items()
                )
            elif isinstance(v, list):
                items.append((new_key, str(v)))
            else:
                items.append((new_key, v))
        return dict(items)
    
    @staticmethod
    def merge_dicts(dict1: dict, dict2: dict, deep: bool = True) -> dict:
        """Merge two dictionaries."""
        if not deep:
            return {**dict1, **dict2}
        
        result = dict1.copy()
        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = DataHelper.merge_dicts(result[key], value, deep=True)
            else:
                result[key] = value
        return result


class MathHelper:
    """Mathematical helpers."""
    
    @staticmethod
    def normalize_array(arr: np.ndarray, min_val: float = 0, max_val: float = 1) -> np.ndarray:
        """Normalize numpy array to range."""
        arr_min, arr_max = arr.min(), arr.max()
        if arr_max == arr_min:
            return np.full_like(arr, (min_val + max_val) / 2, dtype=float)
        normalized = (arr - arr_min) / (arr_max - arr_min)
        return normalized * (max_val - min_val) + min_val
    
    @staticmethod
    def compute_iou(mask1: np.ndarray, mask2: np.ndarray) -> float:
        """Compute Intersection over Union (IoU)."""
        intersection = np.logical_and(mask1, mask2).sum()
        union = np.logical_or(mask1, mask2).sum()
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    @staticmethod
    def compute_dice(mask1: np.ndarray, mask2: np.ndarray) -> float:
        """Compute Dice coefficient."""
        intersection = np.logical_and(mask1, mask2).sum()
        return 2.0 * intersection / (mask1.sum() + mask2.sum())
    
    @staticmethod
    def compute_metrics(
        y_true: np.ndarray,
        y_pred: np.ndarray
    ) -> dict:
        """Compute classification metrics."""
        tp = np.sum(np.logical_and(y_true == 1, y_pred == 1))
        tn = np.sum(np.logical_and(y_true == 0, y_pred == 0))
        fp = np.sum(np.logical_and(y_true == 0, y_pred == 1))
        fn = np.sum(np.logical_and(y_true == 1, y_pred == 0))
        
        accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "tp": int(tp),
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn)
        }


class StringHelper:
    """String manipulation helpers."""
    
    @staticmethod
    def truncate(text: str, length: int, suffix: str = "...") -> str:
        """Truncate string to length."""
        if len(text) <= length:
            return text
        return text[:length - len(suffix)] + suffix
    
    @staticmethod
    def camel_to_snake(name: str) -> str:
        """Convert camelCase to snake_case."""
        import re
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
    
    @staticmethod
    def snake_to_camel(name: str) -> str:
        """Convert snake_case to camelCase."""
        components = name.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])
    
    @staticmethod
    def generate_hash(text: str, algorithm: str = "sha256") -> str:
        """Generate hash of text."""
        if algorithm == "md5":
            return hashlib.md5(text.encode()).hexdigest()
        elif algorithm == "sha1":
            return hashlib.sha1(text.encode()).hexdigest()
        else:
            return hashlib.sha256(text.encode()).hexdigest()


class TimeHelper:
    """Time utilities."""
    
    @staticmethod
    def get_timestamp() -> str:
        """Get current timestamp as ISO string."""
        return datetime.now().isoformat()
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format seconds as human-readable duration."""
        if seconds < 1:
            return f"{seconds * 1000:.0f}ms"
        elif seconds < 60:
            return f"{seconds:.1f}s"
        else:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
    
    @staticmethod
    def time_it(func):
        """Decorator to time function execution."""
        def wrapper(*args, **kwargs):
            import time
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start
            logger.debug(f"{func.__name__} took {TimeHelper.format_duration(duration)}")
            return result
        return wrapper


class ValidationHelper:
    """Validation helpers."""
    
    @staticmethod
    def is_numeric(value: Any) -> bool:
        """Check if value is numeric."""
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if string is valid URL."""
        import re
        pattern = r"^https?://[^\s/$.?#].[^\s]*$"
        return bool(re.match(pattern, url))
    
    @staticmethod
    def get_nested_value(d: dict, keys: List[str], default: Any = None) -> Any:
        """Get value from nested dictionary."""
        for key in keys:
            if isinstance(d, dict):
                d = d.get(key, {})
            else:
                return default
        return d if isinstance(d, dict) is False else default
