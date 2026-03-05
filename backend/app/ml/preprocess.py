import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import io
import requests

def get_preprocessing_transforms():
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

def download_image(image_url: str) -> Image.Image:
    response = requests.get(image_url, timeout=10)
    response.raise_for_status()
    image = Image.open(io.BytesIO(response.content)).convert('RGB')
    return image

def preprocess_image(image_path_or_url: str) -> torch.Tensor:
    if image_path_or_url.startswith(('http://', 'https://')):
        image = download_image(image_path_or_url)
    else:
        image = Image.open(image_path_or_url).convert('RGB')
    
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
