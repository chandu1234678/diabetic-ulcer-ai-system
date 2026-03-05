import numpy as np
from PIL import Image
import requests
import io
import os

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")

def resolve_image_path(image_url: str) -> str:
    if image_url.startswith("/uploads/"):
        filename = image_url.replace("/uploads/", "")
        return os.path.join(UPLOAD_DIR, filename)
    if image_url.startswith("local://"):
        filename = image_url.replace("local://", "")
        return os.path.join(UPLOAD_DIR, filename)
    return image_url

def estimate_ulcer_area(image_url: str) -> float:
    resolved = resolve_image_path(image_url)
    if resolved.startswith(('http://', 'https://')):
        response = requests.get(resolved, timeout=10)
        response.raise_for_status()
        image = Image.open(io.BytesIO(response.content)).convert('RGB')
    else:
        image = Image.open(resolved).convert('RGB')
    
    image_array = np.array(image)
    
    hsv_image = Image.fromarray(image_array.astype('uint8')).convert('HSV')
    hsv_array = np.array(hsv_image)
    
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([30, 255, 255])
    
    mask = np.all((hsv_array >= lower_red) & (hsv_array <= upper_red), axis=2)
    
    ulcer_pixels = np.sum(mask)
    total_pixels = image_array.shape[0] * image_array.shape[1]
    
    ulcer_area_fraction = ulcer_pixels / total_pixels
    
    return min(ulcer_area_fraction, 1.0)
