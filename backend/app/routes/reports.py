from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.report_service import generate_prediction_report
from app.auth.dependencies import get_current_user
from app.models import User

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/predictions")
def get_prediction_report(patient_id: int = Query(None), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    report = generate_prediction_report(db=db, user_id=user.id, patient_id=patient_id)
    return report
