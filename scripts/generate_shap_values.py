"""
Generate SHAP values for model explainability
"""

import argparse
import json
import logging
from pathlib import Path
from typing import Dict, Any

import numpy as np
import torch
from PIL import Image
import shap

logger = logging.getLogger(__name__)


class SHAPExplainer:
    """Generate SHAP values for model predictions"""
    
    def __init__(self, model_path: str, device: str = "cuda"):
        self.device = device
        self.model = self._load_model(model_path)
        self.model.to(device)
        self.model.eval()
    
    def _load_model(self, model_path: str):
        """Load trained model"""
        logger.info(f"Loading model from {model_path}")
        # Placeholder - implement with actual model loading
        return None
    
    def generate_shap_values(
        self,
        image_path: str,
        background_data: np.ndarray = None,
        num_samples: int = 100
    ) -> Dict[str, Any]:
        """
        Generate SHAP values for an image
        
        Args:
            image_path: Path to input image
            background_data: Background data for SHAP
            num_samples: Number of samples for SHAP approximation
            
        Returns:
            Dictionary containing SHAP values and explanations
        """
        
        logger.info(f"Generating SHAP values for {image_path}")
        
        # Load image
        image = Image.open(image_path).convert('RGB')
        image_array = np.array(image) / 255.0
        
        # Normalize
        image_tensor = torch.from_numpy(image_array).float().unsqueeze(0)
        image_tensor = image_tensor.to(self.device)
        
        # Create SHAP explainer
        # In production, use actual SHAP library
        # explainer = shap.GradientExplainer(self.model, background_data)
        
        # Get prediction
        with torch.no_grad():
            prediction = self.model(image_tensor)
        
        # Generate dummy SHAP values for demonstration
        shap_values = np.random.randn(*image_array.shape) * 0.1
        
        return {
            "image_path": str(image_path),
            "prediction": float(prediction.item()),
            "shap_values": shap_values.tolist(),
            "feature_importance": self._calculate_feature_importance(shap_values)
        }
    
    def _calculate_feature_importance(self, shap_values: np.ndarray) -> Dict[str, float]:
        """Calculate feature importance from SHAP values"""
        
        # Calculate mean absolute SHAP values per channel
        shap_abs = np.abs(shap_values)
        
        if len(shap_values.shape) == 3:
            # Per channel importance
            importance = {
                "red_channel": float(np.mean(shap_abs[0])),
                "green_channel": float(np.mean(shap_abs[1])),
                "blue_channel": float(np.mean(shap_abs[2]))
            }
        else:
            importance = {"overall": float(np.mean(shap_abs))}
        
        return importance


def generate_batch_shap_values(
    image_dir: str,
    model_path: str,
    output_dir: str = "shap_explanations",
    device: str = "cuda"
):
    """
    Generate SHAP values for all images in a directory
    
    Args:
        image_dir: Directory containing images
        model_path: Path to trained model
        output_dir: Directory to save SHAP values
        device: Device to use
    """
    
    logger.info(f"Generating SHAP values for images in {image_dir}")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)
    
    # Initialize explainer
    explainer = SHAPExplainer(model_path, device=device)
    
    # Get image files
    image_dir_path = Path(image_dir)
    image_files = (
        list(image_dir_path.glob("*.jpg")) +
        list(image_dir_path.glob("*.png")) +
        list(image_dir_path.glob("*.JPEG"))
    )
    
    logger.info(f"Found {len(image_files)} images")
    
    shap_results = []
    
    for idx, image_file in enumerate(image_files):
        try:
            logger.info(f"Processing {idx+1}/{len(image_files)}: {image_file.name}")
            
            shap_data = explainer.generate_shap_values(str(image_file))
            shap_results.append(shap_data)
            
        except Exception as e:
            logger.error(f"Error processing {image_file}: {str(e)}")
            continue
    
    # Save results
    results_file = output_path / "shap_values.json"
    with open(results_file, 'w') as f:
        json.dump(shap_results, f, indent=2)
    
    logger.info(f"Saved SHAP values to {results_file}")
    
    # Generate summary statistics
    summary = {
        "total_images": len(image_files),
        "processed_images": len(shap_results),
        "average_prediction": np.mean([r["prediction"] for r in shap_results]),
        "feature_importance_summary": _aggregate_importance(shap_results)
    }
    
    summary_file = output_path / "summary.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    logger.info(f"Saved summary to {summary_file}")
    
    return shap_results


def _aggregate_importance(results: list) -> Dict[str, float]:
    """Aggregate feature importance across all results"""
    if not results:
        return {}
    
    importances = [r["feature_importance"] for r in results]
    
    # Calculate mean importance for each feature
    aggregated = {}
    for key in importances[0].keys():
        values = [imp[key] for imp in importances if key in imp]
        if values:
            aggregated[key] = float(np.mean(values))
    
    return aggregated


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate SHAP values for model explanations")
    parser.add_argument("--image-dir", type=str, default="datasets/images/ulcers",
                        help="Path to image directory")
    parser.add_argument("--model-path", type=str, default="model_weights/cnn_ulcer_model.pth",
                        help="Path to trained model")
    parser.add_argument("--output-dir", type=str, default="shap_explanations",
                        help="Directory to save SHAP values")
    parser.add_argument("--device", type=str, default="cuda",
                        help="Device to use (cuda or cpu)")
    
    args = parser.parse_args()
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )
    
    generate_batch_shap_values(
        image_dir=args.image_dir,
        model_path=args.model_path,
        output_dir=args.output_dir,
        device=args.device
    )
