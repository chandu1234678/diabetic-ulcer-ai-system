import numpy as np
import shap
import torch

class ShapExplainer:
    def __init__(self, model, background_data=None, num_background_samples=100):
        self.model = model
        self.background_data = background_data
        self.num_background_samples = num_background_samples
    
    def explain_clinical_features(self, clinical_data, feature_names):
        explainer = shap.KernelExplainer(
            self._predict_fn,
            np.random.randn(self.num_background_samples, clinical_data.shape[1])
        )
        
        shap_values = explainer.shap_values(clinical_data)
        
        if isinstance(shap_values, list):
            shap_values = shap_values[1]
        
        importance_dict = {}
        for i, name in enumerate(feature_names):
            importance_dict[name] = float(np.abs(shap_values[0, i]))
        
        return importance_dict
    
    def _predict_fn(self, X):
        X_tensor = torch.from_numpy(X).float()
        with torch.no_grad():
            predictions = self.model(X_tensor)
            if len(predictions.shape) > 1:
                predictions = torch.softmax(predictions, dim=1)
                predictions = predictions[:, 1].numpy()
            else:
                predictions = predictions.numpy()
        return predictions

def generate_shap_values(model, clinical_features, feature_names):
    explainer = ShapExplainer(model)
    importance = explainer.explain_clinical_features(clinical_features, feature_names)
    return importance
