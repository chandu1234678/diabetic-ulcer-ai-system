from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import PredictionRequest, PredictionResponse
from app.services.inference_service import run_inference
from app.services.report_service import save_prediction_log
from app.auth.dependencies import get_current_user
from app.models import User
from app.monitoring.metrics import track_prediction, track_inference_time
import time

router = APIRouter(prefix="/predict", tags=["prediction"])

@router.post("/", response_model=PredictionResponse)
async def predict(request: PredictionRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    start_time = time.time()
    
    result = run_inference(
        image_url=request.image_url,
        age=request.age,
        bmi=request.bmi,
        diabetes_duration=request.diabetes_duration,
        infection_signs=request.infection_signs
    )
    
    inference_time = time.time() - start_time
    track_prediction("multimodal")
    track_inference_time("multimodal", inference_time)
    
    save_prediction_log(
        db=db,
        user_id=user.id,
        patient_id=request.patient_id,
        prediction=result["prediction"],
        confidence=result["confidence"],
        image_url=request.image_url
    )
    
    return PredictionResponse(
        prediction=result["prediction"],
        confidence=result["confidence"],
        gradcam_heatmap=result["gradcam_heatmap"],
        shap_importance=result["shap_importance"],
        image_url=result["image_url"]
    )
