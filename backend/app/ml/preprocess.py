import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import io
import os
import requests

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")

def get_preprocessing_transforms():
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

def resolve_image_path(image_path_or_url: str) -> str:
    """Resolve image path: /uploads/file -> local path, http -> URL, else local path."""
    if image_path_or_url.startswith("/uploads/"):
        filename = image_path_or_url.replace("/uploads/", "")
        return os.path.join(UPLOAD_DIR, filename)
    if image_path_or_url.startswith("local://"):
        filename = image_path_or_url.replace("local://", "")
        return os.path.join(UPLOAD_DIR, filename)
    return image_path_or_url

def download_image(image_url: str) -> Image.Image:
    response = requests.get(image_url, timeout=10)
    response.raise_for_status()
    image = Image.open(io.BytesIO(response.content)).convert('RGB')
    return image

def preprocess_image(image_path_or_url: str) -> torch.Tensor:
    resolved = resolve_image_path(image_path_or_url)
    if resolved.startswith(('http://', 'https://')):
        image = download_image(resolved)
    else:
        image = Image.open(resolved).convert('RGB')
    
    transforms_pipeline = get_preprocessing_transforms()
    tensor = transforms_pipeline(image)
    
    return tensor.unsqueeze(0)

def preprocess_clinical_data(age: int, bmi: float, diabetes_duration: int, infection_signs: str) -> torch.Tensor:
    infection_map = {
        "none": 0.0,
        "mild": 0.33,
        "moderate": 0.66,
        "severe": 1.0
    }
    
    infection_value = infection_map.get(infection_signs.lower(), 0.0)
    
    clinical_features = torch.tensor([
        [age / 100.0, bmi / 50.0, diabetes_duration / 50.0, infection_value]
    ], dtype=torch.float32)
    
    return clinical_features
