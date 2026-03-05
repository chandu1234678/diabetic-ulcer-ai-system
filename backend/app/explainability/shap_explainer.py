"""SHAP (SHapley Additive exPlanations) explainability."""

import numpy as np
import torch
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


class SHAPExplainer:
    """
    SHAP-based explanation for model predictions.
    
    Uses Shapley values to compute feature importance based on
    cooperative game theory.
    """
    
    def __init__(
        self,
        model: torch.nn.Module,
        background_samples: Optional[np.ndarray] = None,
        n_samples: int = 100
    ):
        """
        Initialize SHAP explainer.
        
        Args:
            model: PyTorch model
            background_samples: Background data for baseline
            n_samples: Number of samples for approximation
        """
        self.model = model
        self.background_samples = background_samples
        self.n_samples = n_samples
        self.device = next(model.parameters()).device
    
    def explain_prediction(
        self,
        input_tensor: torch.Tensor,
        target_class: Optional[int] = None
    ) -> dict:
        """
        Generate SHAP explanation for prediction.
        
        Args:
            input_tensor: Input image tensor
            target_class: Target class for explanation
        
        Returns:
            Dictionary with SHAP values and feature importance
        """
        try:
            self.model.eval()
            
            with torch.no_grad():
                # Get baseline prediction
                baseline_output = self.model(self.background_samples.to(self.device))
                baseline_pred = torch.mean(baseline_output, dim=0)
            
            # Approximate SHAP values
            shap_values = self._approximate_shap_values(input_tensor, target_class)
            
            # Compute feature importance
            feature_importance = np.abs(shap_values).mean(axis=(1, 2))
            
            logger.debug(f"Generated SHAP explanation for class {target_class}")
            
            return {
                "shap_values": shap_values.tolist(),
                "feature_importance": feature_importance.tolist(),
                "baseline_prediction": baseline_pred.cpu().numpy().tolist()
            }
        
        except Exception as e:
            logger.error(f"Error in SHAP explanation: {str(e)}")
            raise
    
    def _approximate_shap_values(
        self,
        input_tensor: torch.Tensor,
        target_class: Optional[int] = None
    ) -> np.ndarray:
        """
        Approximate SHAP values using sampling.
        
        Args:
            input_tensor: Input tensor
            target_class: Target class
        
        Returns:
            Approximate SHAP values
        """
        shap_values = np.zeros_like(input_tensor.cpu().numpy()[0])
        
        # Sample-based approximation
        for _ in range(self.n_samples):
            # Create masked input
            mask = np.random.binomial(1, 0.5, size=input_tensor.shape)
            masked_input = input_tensor * torch.from_numpy(mask).to(input_tensor.device)
            
            # Get prediction
            with torch.no_grad():
                output = self.model(masked_input)
                if target_class is not None:
                    pred = output[0, target_class]
                else:
                    pred = torch.max(output[0])
            
            # Accumulate
            shap_values += (mask[0] - 0.5) * pred.cpu().numpy()
        
        return shap_values / self.n_samples
    
    def plot_explanation(
        self,
        image: np.ndarray,
        shap_values: np.ndarray
    ) -> dict:
        """
        Generate visualization data for SHAP explanation.
        
        Args:
            image: Original image
            shap_values: SHAP values
        
        Returns:
            Visualization data
        """
        # Normalize SHAP values
        shap_normalized = (shap_values - shap_values.min()) / (
            shap_values.max() - shap_values.min() + 1e-8
        )
        
        return {
            "original_image": image.tolist(),
            "shap_heatmap": shap_normalized.tolist(),
            "positive_impact": np.maximum(shap_values, 0).tolist(),
            "negative_impact": np.maximum(-shap_values, 0).tolist()
        }


class ShapleyValueCalculator:
    """Calculate exact Shapley values for subsets."""
    
    @staticmethod
    def calculate_shapley_value(
        feature_idx: int,
        model_fn,
        feature_matrix: np.ndarray,
        target_class: int,
        n_samples: int = 100
    ) -> float:
        """
        Calculate Shapley value for a single feature.
        
        Args:
            feature_idx: Feature index
            model_fn: Model prediction function
            feature_matrix: Input feature matrix
            target_class: Target class
            n_samples: Number of Monte Carlo samples
        
        Returns:
            Shapley value
        """
        shapley_value = 0
        n_features = feature_matrix.shape[1]
        
        for _ in range(n_samples):
            # Random permutation
            perm = np.random.permutation(n_features)
            
            # Find position of feature in permutation
            idx = np.where(perm == feature_idx)[0][0]
            
            # Compute marginal contribution
            # Prediction without feature
            features_without = perm[:idx]
            pred_without = model_fn(feature_matrix[:, features_without])
            
            # Prediction with feature
            features_with = perm[:idx + 1]
            pred_with = model_fn(feature_matrix[:, features_with])
            
            marginal_contrib = pred_with[target_class] - pred_without[target_class]
            shapley_value += marginal_contrib
        
        return shapley_value / n_samples


def create_shap_explainer(
    model: torch.nn.Module,
    background_samples: Optional[np.ndarray] = None,
    **kwargs
) -> SHAPExplainer:
    """Create SHAP explainer."""
    return SHAPExplainer(model, background_samples, **kwargs)
