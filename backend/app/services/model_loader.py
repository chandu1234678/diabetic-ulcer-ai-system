import torch
import os
from app.ml.cnn_model import create_model
from app.ml.multimodal_model import create_multimodal_model
from app.config import settings
import logging

logger = logging.getLogger(__name__)

_cnn_model = None
_multimodal_model = None
_segmentation_model = None

def load_cnn_model():
    global _cnn_model
    
    if _cnn_model is not None:
        return _cnn_model
    
    model = create_model(num_classes=2, pretrained=True)
    
    if os.path.exists(settings.cnn_model_path):
        try:
            checkpoint = torch.load(settings.cnn_model_path, map_location='cpu')
            model.load_state_dict(checkpoint)
        except:
            logger.warning(f"Could not load checkpoint from {settings.cnn_model_path}, using pretrained")
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    model.eval()
    
    _cnn_model = model
    return model

def load_multimodal_model():
    global _multimodal_model
    
    if _multimodal_model is not None:
        return _multimodal_model
    
    model = create_multimodal_model(image_feature_dim=2048, num_clinical_features=4, num_classes=2)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    model.eval()
    
    _multimodal_model = model
    return model

def load_segmentation_model():
    """Load or retrieve the segmentation model."""
    global _segmentation_model
    
    if _segmentation_model is not None:
        return _segmentation_model
    
    try:
        from app.ml.segmentation_model import create_segmentation_model
        
        model = create_segmentation_model(num_classes=2)
        
        if os.path.exists(settings.segmentation_model_path):
            try:
                checkpoint = torch.load(settings.segmentation_model_path, map_location='cpu')
                model.load_state_dict(checkpoint)
                logger.info(f"Loaded segmentation model weights from {settings.segmentation_model_path}")
            except Exception as e:
                logger.warning(f"Could not load segmentation model checkpoint: {e}")
        else:
            logger.warning(f"Segmentation model weights not found at {settings.segmentation_model_path}")
        
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = model.to(device)
        model.eval()
        
        _segmentation_model = model
        return model
    except Exception as e:
        logger.error(f"Error loading segmentation model: {e}")
        return None

def get_model(model_type: str = "cnn"):
    if model_type == "cnn":
        return load_cnn_model()
    elif model_type == "multimodal":
        return load_multimodal_model()
    elif model_type == "segmentation":
        return load_segmentation_model()
    else:
        return load_cnn_model()

def get_segmentation_model():
    """Get segmentation model instance."""
    return load_segmentation_model()
