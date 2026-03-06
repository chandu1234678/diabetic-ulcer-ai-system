"""Package for model definitions and utilities."""

# Expose data model classes for easy imports
from .models import User, Patient, PredictionLog, UlcerImage

# Also include model architecture helpers
from .cnn_ulcer_model import CNNUlcerModel, create_cnn_model
from .segmentation_model import create_segmentation_model
from .multimodal_model import MultimodalModel, create_multimodal_model

# loader utilities are expensive and depend on settings, so import them lazily


def get_cnn_model(*args, **kwargs):
    from .load_model import get_cnn_model as _get
    return _get(*args, **kwargs)


def get_segmentation_model(*args, **kwargs):
    from .load_model import get_segmentation_model as _get
    return _get(*args, **kwargs)


def get_multimodal_model(*args, **kwargs):
    from .load_model import get_multimodal_model as _get
    return _get(*args, **kwargs)


def clear_model_cache():
    from .load_model import ModelLoader
    ModelLoader.clear_cache()
