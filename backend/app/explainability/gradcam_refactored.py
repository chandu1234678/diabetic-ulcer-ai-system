import torch
import torch.nn.functional as F
import numpy as np
import cv2
import os
import sys
from PIL import Image
import torchvision.transforms as transforms


class GradCAM:
    """
    Grad-CAM implementation for ResNet18.
    Generates visual explanations for model predictions by computing class-specific 
    gradient-weighted feature maps.
    """
    
    def __init__(self, model, target_layer):
        """
        Initialize Grad-CAM.
        
        Args:
            model: PyTorch model (e.g., ResNet18)
            target_layer: The layer to compute gradients for (e.g., model.layer4[-1])
        """
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        
        # Register hooks to capture activations and gradients
        self.target_layer.register_forward_hook(self._save_activations)
        self.target_layer.register_full_backward_hook(self._save_gradients)
    
    def _save_activations(self, module, input, output):
        """Hook to save feature activations from forward pass."""
        self.activations = output.detach()
    
    def _save_gradients(self, module, grad_input, grad_output):
        """Hook to save gradients from backward pass."""
        self.gradients = grad_output[0].detach()
    
    def generate_heatmap(self, input_tensor, target_class=None):
        """
        Generate Grad-CAM heatmap following the original algorithm.
        
        Algorithm steps:
        1. Forward pass: Get activations from target layer
        2. Backward pass: Compute gradients of target class score
        3. Global average pool: Average gradients across spatial dimensions
        4. Weight channels: Multiply each channel's activation by its gradient
        5. Sum channels: Aggregate weighted activations
        6. Apply ReLU: Keep only positive contributions
        7. Normalize: Scale to [0, 1] range
        8. Resize: Match input image size
        
        Args:
            input_tensor: Input image tensor (B, C, H, W)
            target_class: Target class index (for multi-class). If None, uses predicted class.
        
        Returns:
            np.ndarray: Grad-CAM heatmap (H, W) as uint8 (0-255)
        """
        self.model.eval()
        
        with torch.enable_grad():
            input_tensor.requires_grad_(True)
            output = self.model(input_tensor)
            
            # Determine target class if not specified
            if target_class is None:
                target_class = output.argmax(dim=1).item()
            
            # Compute gradients of target class score
            self.model.zero_grad()
            score = output[0, target_class]
            score.backward()
        
        # Grad-CAM computation (from original paper)
        # w_k = 1/Z * sum_xy(∂y^c/∂A^k_xy)
        pooled_gradients = torch.mean(self.gradients, dim=[0, 2, 3])
        
        # L^c = ReLU(sum_k w_k * A^k)
        activations = self.activations[0]
        weighted_activations = activations.clone()
        for i in range(weighted_activations.shape[0]):
            weighted_activations[i, :, :] *= pooled_gradients[i]
        
        # Sum across channels
        heatmap = torch.mean(weighted_activations, dim=0).cpu().numpy()
        
        # Apply ReLU to keep only positive contributions
        heatmap = np.maximum(heatmap, 0)
        
        # Normalize to [0, 1]
        heatmap_max = heatmap.max()
        if heatmap_max > 1e-8:
            heatmap = heatmap / heatmap_max
        
        # Resize to 224x224 for consistency
        heatmap_resized = cv2.resize(heatmap, (224, 224))
        
        # Convert to uint8 [0, 255]
        heatmap_uint8 = np.uint8(255 * heatmap_resized)
        
        return heatmap_uint8


def generate_gradcam_from_tensor(model, input_tensor, target_layer=None):
    """
    Generate Grad-CAM heatmap from a pre-loaded model and input tensor.
    
    **Use this function during inference** when you already have the model loaded 
    and the image tensor preprocessed.
    
    Args:
        model: Loaded PyTorch model (ResNet18)
        input_tensor: Preprocessed input tensor (B, C, H, W)
        target_layer: Target layer for Grad-CAM. Defaults to model.resnet.layer4[-1]
    
    Returns:
        np.ndarray: Grad-CAM heatmap (224, 224) as uint8
    """
    if target_layer is None:
        target_layer = model.resnet.layer4[-1]
    
    gradcam = GradCAM(model, target_layer)
    heatmap = gradcam.generate_heatmap(input_tensor)
    
    return heatmap


def generate_gradcam(image_path, model_path):
    """
    Generate Grad-CAM heatmap for an image using a trained ResNet18 model.
    
    **Use this function for standalone inference** (e.g., testing or batch processing).
    
    This function handles:
    - Loading the model from a checkpoint
    - Preprocessing the image
    - Generating the heatmap
    - Creating an overlay
    - Saving the result
    
    Args:
        image_path (str): Path to the input image
        model_path (str): Path to the saved model checkpoint (best_dfu_model.pth)
    
    Returns:
        tuple: (predicted_class, confidence, overlay_image_np)
               - predicted_class: "normal" or "ulcer"
               - confidence: float in [0, 1]
               - overlay_image_np: np.ndarray BGR image with heatmap overlay
    """
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from app.ml.cnn_model import create_model
    
    # Load model
    model = create_model(num_classes=2, pretrained=False)
    checkpoint = torch.load(model_path, map_location='cpu')
    model.load_state_dict(checkpoint)
    model.eval()
    device = torch.device('cpu')
    model = model.to(device)
    
    # Load and preprocess image
    image = Image.open(image_path).convert('RGB')
    original_size = image.size  # (width, height)
    
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    
    input_tensor = transform(image).unsqueeze(0).to(device)
    
    # Get prediction
    with torch.no_grad():
        outputs = model(input_tensor)
        predicted_class_idx = outputs.argmax(dim=1).item()
        confidence = torch.softmax(outputs, dim=1)[0, predicted_class_idx].item()
    
    class_names = ['normal', 'ulcer']
    predicted_class = class_names[predicted_class_idx]
    
    # Generate Grad-CAM heatmap
    heatmap = generate_gradcam_from_tensor(model, input_tensor, model.resnet.layer4[-1])
    
    # Resize heatmap to original image size
    heatmap_resized = cv2.resize(heatmap, (original_size[0], original_size[1]))
    
    # Load original image as numpy array
    img_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Apply colormap to heatmap
    heatmap_colored = cv2.applyColorMap(heatmap_resized, cv2.COLORMAP_JET)
    
    # Blend original image with heatmap (60% original, 40% heatmap)
    overlay = cv2.addWeighted(img_array, 0.6, heatmap_colored, 0.4, 0)
    
    # Save result
    os.makedirs('outputs', exist_ok=True)
    cv2.imwrite('outputs/gradcam_result.png', overlay)
    
    return predicted_class, confidence, overlay
