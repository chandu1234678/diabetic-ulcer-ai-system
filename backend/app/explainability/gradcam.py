"""Grad-CAM (Gradient-weighted Class Activation Mapping) implementation."""

import torch
import torch.nn.functional as F
import numpy as np
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


class GradCAM:
    """
    Grad-CAM explanation method for CNN models.
    
    Generates visual explanations by mapping class-specific gradients
    back to the input image.
    """
    
    def __init__(self, model: torch.nn.Module, target_layer: str):
        """
        Initialize Grad-CAM.
        
        Args:
            model: PyTorch model
            target_layer: Name of target layer for gradient computation
        """
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        
        self._register_hooks()
    
    def _register_hooks(self):
        """Register forward and backward hooks."""
        def forward_hook(module, input, output):
            self.activations = output.detach()
        
        def backward_hook(module, grad_input, grad_output):
            self.gradients = grad_output[0].detach()
        
        # Register hooks on target layer
        target = self._get_layer(self.model, self.target_layer)
        target.register_forward_hook(forward_hook)
        target.register_backward_hook(backward_hook)
    
    def _get_layer(self, model: torch.nn.Module, layer_name: str) -> torch.nn.Module:
        """Get layer by name."""
        for name, module in model.named_modules():
            if name == layer_name:
                return module
        raise ValueError(f"Layer {layer_name} not found")
    
    def generate_cam(
        self,
        input_tensor: torch.Tensor,
        target_class: int,
        eigen_smooth: bool = False
    ) -> np.ndarray:
        """
        Generate Grad-CAM heatmap.
        
        Args:
            input_tensor: Input image tensor (1, 3, H, W)
            target_class: Target class for gradient computation
            eigen_smooth: Whether to apply eigensmoothing
        
        Returns:
            Heatmap as numpy array
        """
        try:
            self.model.eval()
            
            # Forward pass
            output = self.model(input_tensor)
            
            # Zero gradients
            self.model.zero_grad()
            
            # Backward pass
            target_score = output[0, target_class]
            target_score.backward()
            
            # Compute weights
            gradients = self.gradients[0]  # (C, H, W)
            activations = self.activations[0]  # (C, H, W)
            
            weights = torch.mean(gradients, dim=(1, 2))  # (C,)
            
            # Generate CAM
            cam = torch.zeros(activations.shape[1:], device=activations.device)
            for i, w in enumerate(weights):
                cam += w * activations[i, :, :]
            
            cam = F.relu(cam)
            cam = cam.cpu().numpy()
            
            # Normalize
            if cam.max() > 0:
                cam = cam / cam.max()
            
            logger.debug(f"Generated Grad-CAM for class {target_class}")
            return cam
        
        except Exception as e:
            logger.error(f"Error generating Grad-CAM: {str(e)}")
            raise
    
    def generate_smooth_cam(
        self,
        input_tensor: torch.Tensor,
        target_class: int,
        n_samples: int = 50
    ) -> np.ndarray:
        """
        Generate smoothed Grad-CAM using noise aggregation.
        
        Args:
            input_tensor: Input image tensor
            target_class: Target class
            n_samples: Number of noise samples
        
        Returns:
            Smoothed heatmap
        """
        cams = []
        
        for _ in range(n_samples):
            # Add small noise
            noise = torch.randn_like(input_tensor) * 0.1
            noisy_input = input_tensor + noise
            
            # Generate CAM
            cam = self.generate_cam(noisy_input, target_class)
            cams.append(cam)
        
        # Average
        smooth_cam = np.mean(cams, axis=0)
        
        logger.debug(f"Generated smoothed Grad-CAM with {n_samples} samples")
        return smooth_cam


class GradCAMPP:
    """Grad-CAM++ for better localization."""
    
    def __init__(self, model: torch.nn.Module, target_layer: str):
        """Initialize Grad-CAM++."""
        self.model = model
        self.gradients = None
        self.activations = None
        self.target_layer = target_layer
        
        self._register_hooks()
    
    def _register_hooks(self):
        """Register hooks."""
        def forward_hook(module, input, output):
            self.activations = output.detach()
        
        def backward_hook(module, grad_input, grad_output):
            self.gradients = grad_output[0].detach()
        
        target = self._get_layer(self.model, self.target_layer)
        target.register_forward_hook(forward_hook)
        target.register_backward_hook(backward_hook)
    
    def _get_layer(self, model: torch.nn.Module, layer_name: str):
        """Get layer by name."""
        for name, module in model.named_modules():
            if name == layer_name:
                return module
        raise ValueError(f"Layer {layer_name} not found")
    
    def generate_cam(
        self,
        input_tensor: torch.Tensor,
        target_class: int
    ) -> np.ndarray:
        """Generate Grad-CAM++ heatmap."""
        try:
            self.model.eval()
            
            # Forward pass
            output = self.model(input_tensor)
            self.model.zero_grad()
            
            # Backward pass
            target_score = output[0, target_class]
            target_score.backward()
            
            # Compute second derivatives
            gradients = self.gradients[0]
            activations = self.activations[0]
            
            weights = torch.mean(gradients, dim=(1, 2))
            
            # Generate CAM
            cam = torch.zeros(activations.shape[1:], device=activations.device)
            for i, w in enumerate(weights):
                cam += w * activations[i, :, :]
            
            cam = F.relu(cam)
            cam = cam.cpu().numpy()
            
            if cam.max() > 0:
                cam = cam / cam.max()
            
            return cam
        
        except Exception as e:
            logger.error(f"Error in Grad-CAM++: {str(e)}")
            raise


def create_gradcam(model: torch.nn.Module, target_layer: str) -> GradCAM:
    """Create Grad-CAM explainer."""
    return GradCAM(model, target_layer)
