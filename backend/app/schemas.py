from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PatientBase(BaseModel):
    patient_identifier: str
    age: int
    bmi: float
    diabetes_duration: int
    infection_signs: str = "none"

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PredictionRequest(BaseModel):
    image_url: str
    age: int
    bmi: float
    diabetes_duration: int
    infection_signs: str = "none"
    patient_id: Optional[int] = None

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    gradcam_heatmap: List[List[float]]
    shap_importance: dict
    image_url: str

class UlcerImageResponse(BaseModel):
    id: int
    patient_id: int
    image_url: str
    prediction: str
    confidence: float
    ulcer_area: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class PatientProgressionResponse(BaseModel):
    trend: str
    previous_area: float
    latest_area: float
    percentage_change: float
    total_images: int

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
