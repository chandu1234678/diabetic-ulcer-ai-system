from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
def health_check():
    """Health check endpoint for service monitoring"""
    return {
        "status": "healthy",
        "service": "medvision_ai_diabetic_ulcer_detection",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": "production"
    }

