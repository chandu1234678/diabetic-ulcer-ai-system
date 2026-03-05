import torch
import numpy as np
from app.services.model_loader import get_model
from app.ml.preprocess import preprocess_image, preprocess_clinical_data
from app.ml.ulcer_area_estimator import estimate_ulcer_area
from app.explainability.gradcam import generate_gradcam
from app.explainability.shap_explainer import generate_shap_values
import time


def calculate_risk_score(confidence, age, bmi, diabetes_duration, infection_signs, ulcer_area):
    """Calculate holistic risk score (0-100%) from model output + clinical data."""
    score = 0

    # Model confidence contributes up to 40 points
    if confidence > 0.5:
        score += confidence * 40

    # Age risk (up to 10 points)
    if age > 65:
        score += 10
    elif age > 50:
        score += 5

    # BMI risk (up to 10 points)
    if bmi > 35:
        score += 10
    elif bmi > 30:
        score += 7
    elif bmi > 25:
        score += 3

    # Diabetes duration (up to 15 points)
    if diabetes_duration > 20:
        score += 15
    elif diabetes_duration > 10:
        score += 10
    elif diabetes_duration > 5:
        score += 5

    # Infection (up to 15 points)
    infection_map = {"none": 0, "mild": 5, "moderate": 10, "severe": 15}
    score += infection_map.get(infection_signs.lower(), 0)

    # Ulcer area (up to 10 points)
    if ulcer_area > 20:
        score += 10
    elif ulcer_area > 10:
        score += 7
    elif ulcer_area > 5:
        score += 4

    return min(round(score, 1), 100)


def classify_risk_level(score):
    if score < 20:
        return "Low"
    elif score < 40:
        return "Moderate"
    elif score < 70:
        return "High"
    else:
        return "Very High"


def get_severity(confidence, ulcer_area):
    if confidence < 0.5:
        return "None"
    if ulcer_area > 15 or confidence > 0.9:
        return "Severe"
    if ulcer_area > 8 or confidence > 0.75:
        return "Moderate"
    return "Mild"


def generate_explanation(prediction, confidence, risk_score, risk_level,
                         age, bmi, diabetes_duration, infection_signs,
                         shap_importance, ulcer_area):
    """Generate natural language textual justification for the prediction."""
    lines = []

    if prediction == "ulcer":
        lines.append(
            f"The model detected a diabetic foot ulcer with {confidence*100:.1f}% confidence."
        )
    else:
        lines.append(
            f"The model classified this image as normal skin with {(1-confidence)*100:.1f}% confidence."
        )

    lines.append(f"Overall risk assessment: {risk_level} ({risk_score}%).")

    # Explain top contributing clinical factors
    factors = []
    if age > 60:
        factors.append(f"advanced age ({age} years)")
    if bmi > 30:
        factors.append(f"high BMI ({bmi})")
    if diabetes_duration > 10:
        factors.append(f"long diabetes duration ({diabetes_duration} years)")
    if infection_signs.lower() not in ("none", ""):
        factors.append(f"{infection_signs} infection signs")

    if factors:
        lines.append("Key clinical risk factors: " + ", ".join(factors) + ".")

    # SHAP-based explanation
    if shap_importance:
        sorted_features = sorted(shap_importance.items(), key=lambda x: abs(x[1]), reverse=True)
        top = sorted_features[0]
        lines.append(
            f"The most influential clinical feature was {top[0]} "
            f"(importance: {abs(top[1]):.2f})."
        )

    if prediction == "ulcer" and ulcer_area > 0:
        lines.append(f"Estimated affected area: {ulcer_area:.1f}%.")

    return " ".join(lines)


def get_recommendations(risk_level):
    """Return clinical recommendations based on risk level."""
    recs = {
        "Low": [
            "Continue routine foot care and hygiene",
            "Annual diabetic foot screening recommended"
        ],
        "Moderate": [
            "Increase foot monitoring frequency",
            "Schedule follow-up in 3-6 months",
            "Review blood sugar management with physician"
        ],
        "High": [
            "Intensive wound care protocol recommended",
            "Monthly professional foot assessments",
            "Consider specialist referral (podiatrist/wound care)",
            "Optimize glycemic control immediately"
        ],
        "Very High": [
            "Immediate specialist consultation required",
            "Intensive wound management and possible hospitalization",
            "Daily wound monitoring",
            "Urgent review of all medications and comorbidities"
        ]
    }
    return recs.get(risk_level, [])


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

    # GradCAM
    try:
        gradcam_heatmap = generate_gradcam(cnn_model, image_tensor)
    except Exception as e:
        print(f"GradCAM failed: {e}")
        gradcam_heatmap = [[0.0] * 224 for _ in range(224)]

    # SHAP — pass image_features so multimodal model can be used
    feature_names = ["Age", "BMI", "Diabetes Duration", "Infection Signs"]
    try:
        shap_importance = generate_shap_values(
            multimodal_model, clinical_tensor.cpu().numpy(), feature_names,
            image_features=image_features.cpu()
        )
    except Exception as e:
        print(f"SHAP failed: {e}")
        shap_importance = {n: 0.25 for n in feature_names}

    # Ulcer area
    try:
        ulcer_area = estimate_ulcer_area(image_url)
    except Exception as e:
        print(f"Ulcer area estimation failed: {e}")
        ulcer_area = 0.0

    # Risk assessment
    risk_score = calculate_risk_score(confidence, age, bmi, diabetes_duration, infection_signs, ulcer_area)
    risk_level = classify_risk_level(risk_score)
    severity = get_severity(confidence, ulcer_area)
    recommendations = get_recommendations(risk_level)

    # Textual justification
    explanation_text = generate_explanation(
        prediction, confidence, risk_score, risk_level,
        age, bmi, diabetes_duration, infection_signs,
        shap_importance, ulcer_area
    )

    inference_time = time.time() - start_time

    return {
        "prediction": prediction,
        "confidence": confidence,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "severity": severity,
        "affected_area": ulcer_area,
        "explanation_text": explanation_text,
        "recommendations": recommendations,
        "gradcam_heatmap": gradcam_heatmap,
        "shap_importance": shap_importance,
        "image_url": image_url,
        "inference_time": inference_time
    }
