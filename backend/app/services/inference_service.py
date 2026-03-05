import torch
import numpy as np
from app.services.model_loader import get_model
from app.ml.preprocess import preprocess_image, preprocess_clinical_data
from app.ml.ulcer_area_estimator import estimate_ulcer_area
from app.explainability.gradcam import generate_gradcam
from app.explainability.shap_explainer import generate_shap_values
import time

def run_inference(image_url: str, age: int, bmi: float, diabetes_duration: int, infection_signs: str):
    start_time = time.time()
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    image_tensor = preprocess_image(image_url).to(device)
    clinical_tensor = preprocess_clinical_data(age, bmi, diabetes_duration, infection_signs).to(device)
    
    cnn_model = get_model("cnn")
    multimodal_model = get_model("multimodal")
    
    with torch.no_grad():
        image_features = cnn_model.get_features(image_tensor)
        multi_output = multimodal_model(image_features, clinical_tensor)
        probabilities = torch.softmax(multi_output, dim=1)
        confidence = probabilities[0, 1].item()
    
    prediction = "ulcer" if confidence > 0.5 else "normal"
    
    gradcam_heatmap = generate_gradcam(cnn_model, image_tensor)
    
    feature_names = ["Age", "BMI", "Diabetes Duration", "Infection Signs"]
    shap_importance = generate_shap_values(multimodal_model, clinical_tensor.cpu().numpy(), feature_names)
    
    ulcer_area = estimate_ulcer_area(image_url)
    
    inference_time = time.time() - start_time
    
    return {
        "prediction": prediction,
        "confidence": confidence,
        "gradcam_heatmap": gradcam_heatmap,
        "shap_importance": shap_importance,
        "image_url": image_url,
        "ulcer_area": ulcer_area,
        "inference_time": inference_time
    }
