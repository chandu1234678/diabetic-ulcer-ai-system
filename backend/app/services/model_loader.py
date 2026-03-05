import torch
import os
from app.ml.cnn_model import create_model
from app.ml.multimodal_model import create_multimodal_model
from app.config import settings

_cnn_model = None
_multimodal_model = None

def load_cnn_model():
    global _cnn_model
    
    if _cnn_model is not None:
        return _cnn_model
    
    model = create_model(num_classes=2, pretrained=True)
    
    if os.path.exists(settings.model_path):
        try:
            checkpoint = torch.load(settings.model_path, map_location='cpu')
            model.load_state_dict(checkpoint)
        except:
            print(f"Could not load checkpoint from {settings.model_path}, using pretrained")
    
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

def get_model(model_type: str = "cnn"):
    if model_type == "cnn":
        return load_cnn_model()
    elif model_type == "multimodal":
        return load_multimodal_model()
    else:
        return load_cnn_model()
