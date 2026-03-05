"""Feature importance analysis utilities."""

import numpy as np
import torch
import logging
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)


class FeatureImportance:
    """
    Compute feature importance using various methods.
    
    Methods:
    - Permutation importance
    - Gradient-based importance
    - Attention-based importance
    """
    
    def __init__(self, model: torch.nn.Module):
        """
        Initialize feature importance calculator.
        
        Args:
            model: PyTorch model
        """
        self.model = model
        self.device = next(model.parameters()).device
    
    def permutation_importance(
        self,
        input_tensor: torch.Tensor,
        target_class: int,
        n_repeats: int = 10
    ) -> np.ndarray:
        """
        Calculate permutation importance.
        
        Args:
            input_tensor: Input tensor (1, C, H, W)
            target_class: Target class
            n_repeats: Number of permutation repeats
        
        Returns:
            Importance scores for each feature
        """
        try:
            self.model.eval()
            
            # Get baseline prediction
            with torch.no_grad():
                baseline_output = self.model(input_tensor)
                baseline_score = baseline_output[0, target_class].item()
            
            # Calculate importance for each pixel
            importance = np.zeros(input_tensor.shape[2:])
            
            for h in range(input_tensor.shape[2]):
                for w in range(input_tensor.shape[3]):
                    scores = []
                    
                    for _ in range(n_repeats):
                        # Create permuted input
                        permuted = input_tensor.clone()
                        # Shuffle across channels
                        permuted[0, :, h, w] = permuted[0, :, h, w][torch.randperm(3)]
                        
                        with torch.no_grad():
                            output = self.model(permuted)
                            score = output[0, target_class].item()
                        
                        scores.append(baseline_score - score)
                    
                    importance[h, w] = np.mean(scores)
            
            logger.debug(f"Calculated permutation importance")
            return importance
        
        except Exception as e:
            logger.error(f"Error in permutation importance: {str(e)}")
            raise
    
    def gradient_importance(
        self,
        input_tensor: torch.Tensor,
        target_class: int
    ) -> np.ndarray:
        """
        Calculate gradient-based feature importance.
        
        Args:
            input_tensor: Input tensor
            target_class: Target class
        
        Returns:
            Importance scores
        """
        try:
            input_tensor.requires_grad_(True)
            
            # Forward pass
            output = self.model(input_tensor)
            target_score = output[0, target_class]
            
            # Backward pass
            self.model.zero_grad()
            target_score.backward()
            
            # Get gradients
            gradients = input_tensor.grad.abs()
            
            # Aggregate across channels
            importance = gradients[0].mean(dim=0).cpu().detach().numpy()
            
            logger.debug("Calculated gradient-based importance")
            return importance
        
        except Exception as e:
            logger.error(f"Error in gradient importance: {str(e)}")
            raise
    
    def integrated_gradients(
        self,
        input_tensor: torch.Tensor,
        target_class: int,
        baseline: Optional[torch.Tensor] = None,
        n_steps: int = 50
    ) -> np.ndarray:
        """
        Calculate integrated gradients.
        
        Args:
            input_tensor: Input tensor
            target_class: Target class
            baseline: Baseline input (e.g., black image)
            n_steps: Number of integration steps
        
        Returns:
            Integrated gradients
        """
        try:
            if baseline is None:
                baseline = torch.zeros_like(input_tensor)
            
            integrated_grads = torch.zeros_like(input_tensor)
            
            for i in range(n_steps):
                # Linear interpolation
                alpha = i / n_steps
                interpolated = baseline + alpha * (input_tensor - baseline)
                interpolated.requires_grad_(True)
                
                # Forward pass
                output = self.model(interpolated)
                target_score = output[0, target_class]
                
                # Backward pass
                self.model.zero_grad()
                target_score.backward()
                
                integrated_grads += interpolated.grad
            
            # Average and scale
            integrated_grads = integrated_grads / n_steps
            integrated_grads = (input_tensor - baseline) * integrated_grads
            
            importance = integrated_grads[0].abs().mean(dim=0).cpu().detach().numpy()
            
            logger.debug("Calculated integrated gradients")
            return importance
        
        except Exception as e:
            logger.error(f"Error in integrated gradients: {str(e)}")
            raise
    
    def attention_weights(
        self,
        input_tensor: torch.Tensor
    ) -> Dict[str, np.ndarray]:
        """
        Extract attention weights from attention modules.
        
        Args:
            input_tensor: Input tensor
        
        Returns:
            Dictionary of attention weights by layer
        """
        try:
            attention_maps = {}
            
            # Register hooks to attention modules
            for name, module in self.model.named_modules():
                if 'attention' in name.lower() or 'self_attn' in name.lower():
                    def hook(module, input, output):
                        if isinstance(output, tuple):
                            attention_maps[name] = output[0].cpu().detach().numpy()
                        else:
                            attention_maps[name] = output.cpu().detach().numpy()
                    
                    module.register_forward_hook(hook)
            
            # Forward pass
            with torch.no_grad():
                self.model(input_tensor)
            
            logger.debug(f"Extracted {len(attention_maps)} attention maps")
            return attention_maps
        
        except Exception as e:
            logger.error(f"Error extracting attention weights: {str(e)}")
            raise


def compute_fidelity(
    importance_map: np.ndarray,
    model_fn,
    input_tensor: torch.Tensor,
    target_class: int,
    k: int = 10
) -> float:
    """
    Compute fidelity of importance map.
    
    Measures how well the importance map predicts feature impact.
    
    Args:
        importance_map: Feature importance map
        model_fn: Model prediction function
        input_tensor: Input tensor
        target_class: Target class
        k: Number of top features
    
    Returns:
        Fidelity score
    """
    # Get top-k important pixels
    flat_importance = importance_map.flatten()
    top_indices = np.argsort(flat_importance)[-k:]
    
    # Create masked input
    masked = input_tensor.clone()
    mask = np.zeros_like(importance_map)
    mask.flat[top_indices] = 1
    
    # Apply mask
    h_idx, w_idx = np.where(mask == 0)
    masked[0, :, h_idx, w_idx] = 0
    
    # Compare predictions
    with torch.no_grad():
        original_pred = model_fn(input_tensor)[target_class]
        masked_pred = model_fn(masked)[target_class]
    
    fidelity = max(0, original_pred.item() - masked_pred.item())
    
    return fidelity


def create_feature_importance(model: torch.nn.Module) -> FeatureImportance:
    """Create feature importance calculator."""
    return FeatureImportance(model)
