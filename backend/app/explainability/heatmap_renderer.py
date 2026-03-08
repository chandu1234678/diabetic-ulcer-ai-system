"""Render Grad-CAM heatmaps as overlays on original images."""
import cv2
import numpy as np
import base64
import io
from PIL import Image
from typing import Union, Tuple
import os


def render_heatmap_overlay(
    original_image_path: str,
    heatmap_matrix: Union[np.ndarray, list],
    alpha: float = 0.4,
    colormap: int = cv2.COLORMAP_JET
) -> str:
    """
    Overlay a Grad-CAM heatmap on the original image.
    
    Args:
        original_image_path: Path to original image file or URL
        heatmap_matrix: 2D numpy array or list of heatmap values (0-255 or 0-1)
        alpha: Transparency of overlay (0-1)
        colormap: OpenCV colormap to apply
    
    Returns:
        Base64 encoded image string of the overlay
    """
    # Handle local uploads
    if original_image_path.startswith('/uploads/'):
        filename = original_image_path.split('/')[-1]
        upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads')
        original_image_path = os.path.join(upload_dir, filename)
    
    # Load original image
    if original_image_path.startswith(('http://', 'https://')):
        import requests
        response = requests.get(original_image_path, timeout=10)
        image = Image.open(io.BytesIO(response.content)).convert('RGB')
        img_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    else:
        img_array = cv2.imread(original_image_path)
        if img_array is None:
            raise ValueError(f"Could not load image from {original_image_path}")
    
    # Convert heatmap to numpy array if needed
    if isinstance(heatmap_matrix, list):
        heatmap_array = np.array(heatmap_matrix, dtype=np.uint8)
    else:
        heatmap_array = heatmap_matrix.copy()
    
    # Normalize heatmap to 0-255 if needed
    if heatmap_array.dtype != np.uint8:
        if heatmap_array.max() <= 1.0:
            heatmap_array = (heatmap_array * 255).astype(np.uint8)
        else:
            heatmap_array = np.clip(heatmap_array, 0, 255).astype(np.uint8)
    
    # Resize heatmap to match image size
    heatmap_resized = cv2.resize(heatmap_array, (img_array.shape[1], img_array.shape[0]))
    
    # Apply colormap to heatmap
    heatmap_colored = cv2.applyColorMap(heatmap_resized, colormap)
    
    # Blend original image with heatmap overlay
    overlay = cv2.addWeighted(img_array, 1 - alpha, heatmap_colored, alpha, 0)
    
    # Encode to base64
    ret, buffer = cv2.imencode('.jpg', overlay)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    
    return f"data:image/jpeg;base64,{img_base64}"


def render_heatmap_with_original(
    original_image_path: str,
    heatmap_matrix: Union[np.ndarray, list],
    side_by_side: bool = False
) -> Tuple[str, str]:
    """
    Create both overlay and comparison views.
    
    Returns:
        Tuple of (overlay_base64, comparison_base64) or single overlay if side_by_side=False
    """
    # Load original image
    if original_image_path.startswith(('http://', 'https://')):
        import requests
        response = requests.get(original_image_path, timeout=10)
        image = Image.open(io.BytesIO(response.content)).convert('RGB')
        img_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    else:
        img_array = cv2.imread(original_image_path)
    
    # Convert and normalize heatmap
    if isinstance(heatmap_matrix, list):
        heatmap_array = np.array(heatmap_matrix, dtype=np.uint8)
    else:
        heatmap_array = heatmap_matrix.copy()
    
    if heatmap_array.dtype != np.uint8:
        if heatmap_array.max() <= 1.0:
            heatmap_array = (heatmap_array * 255).astype(np.uint8)
        else:
            heatmap_array = np.clip(heatmap_array, 0, 255).astype(np.uint8)
    
    # Resize heatmap to match image
    heatmap_resized = cv2.resize(heatmap_array, (img_array.shape[1], img_array.shape[0]))
    heatmap_colored = cv2.applyColorMap(heatmap_resized, cv2.COLORMAP_JET)
    
    # Create overlay
    overlay = cv2.addWeighted(img_array, 0.6, heatmap_colored, 0.4, 0)
    ret, buffer = cv2.imencode('.jpg', overlay)
    overlay_base64 = f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"
    
    if side_by_side:
        # Create heatmap-only visualization
        heatmap_only = cv2.applyColorMap(heatmap_resized, cv2.COLORMAP_JET)
        ret, buffer = cv2.imencode('.jpg', heatmap_only)
        heatmap_base64 = f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"
        return overlay_base64, heatmap_base64
    
    return overlay_base64, overlay_base64


def save_heatmap_overlay(
    original_image_path: str,
    heatmap_matrix: Union[np.ndarray, list],
    output_path: str,
    alpha: float = 0.4
) -> str:
    """
    Save overlay as file instead of returning base64.
    
    Returns:
        Path to saved overlay image
    """
    # Load original image
    if original_image_path.startswith(('http://', 'https://')):
        import requests
        response = requests.get(original_image_path, timeout=10)
        image = Image.open(io.BytesIO(response.content)).convert('RGB')
        img_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    else:
        img_array = cv2.imread(original_image_path)
    
    # Convert heatmap
    if isinstance(heatmap_matrix, list):
        heatmap_array = np.array(heatmap_matrix, dtype=np.uint8)
    else:
        heatmap_array = heatmap_matrix.copy()
    
    if heatmap_array.dtype != np.uint8:
        if heatmap_array.max() <= 1.0:
            heatmap_array = (heatmap_array * 255).astype(np.uint8)
        else:
            heatmap_array = np.clip(heatmap_array, 0, 255).astype(np.uint8)
    
    # Resize and create overlay
    heatmap_resized = cv2.resize(heatmap_array, (img_array.shape[1], img_array.shape[0]))
    heatmap_colored = cv2.applyColorMap(heatmap_resized, cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(img_array, 1 - alpha, heatmap_colored, alpha, 0)
    
    # Save
    cv2.imwrite(output_path, overlay)
    return output_path
