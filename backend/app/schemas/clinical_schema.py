"""Clinical data schemas."""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


class ClinicalDataInput(BaseModel):
    """Clinical data input schema."""
    patient_id: str
    age: int = Field(..., ge=0, le=150)
    gender: str = Field(..., regex="^(M|F|Other)$")
    diabetes_type: str = Field(..., regex="^(Type 1|Type 2|Gestational|Other)$")
    duration_of_diabetes: float = Field(..., ge=0)
    hba1c_level: Optional[float] = Field(None, ge=4, le=15)
    bmi: Optional[float] = Field(None, ge=10, le=60)
    smoking_status: Optional[str] = Field(None, regex="^(Never|Former|Active|Unknown)$")
    neuropathy: Optional[bool] = None
    infection_status: Optional[bool] = None
    previous_ulcers: Optional[int] = Field(None, ge=0)
    medications: Optional[List[str]] = None
    comorbidities: Optional[List[str]] = None
    wound_location: Optional[str] = None
    wound_size: Optional[float] = Field(None, ge=0)
    
    class Config:
        schema_extra = {
            "example": {
                "patient_id": "P123456",
                "age": 55,
                "gender": "M",
                "diabetes_type": "Type 2",
                "duration_of_diabetes": 10.5,
                "hba1c_level": 7.8,
                "bmi": 28.5,
                "smoking_status": "Former",
                "neuropathy": True,
                "infection_status": False,
                "previous_ulcers": 1
            }
        }


class ClinicalDataResponse(BaseModel):
    """Clinical data response schema."""
    patient_id: str
    age: int
    gender: str
    diabetes_type: str
    duration_of_diabetes: float
    hba1c_level: Optional[float]
    bmi: Optional[float]
    smoking_status: Optional[str]
    neuropathy: Optional[bool]
    infection_status: Optional[bool]
    previous_ulcers: Optional[int]
    stored_at: datetime


class RiskAssessment(BaseModel):
    """Risk assessment response."""
    patient_id: str
    total_score: float = Field(ge=0, le=100)
    risk_level: str = Field(..., regex="^(Low|Moderate|High|Very High)$")
    risk_factors: List[str]
    recommendations: List[str]
    monitoring_frequency: str
    assessment_date: datetime


class ClinicalDataQuery(BaseModel):
    """Query schema for clinical data."""
    patient_id: Optional[str] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    diabetes_type: Optional[str] = None
    risk_level: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "patient_id": "P123456",
                "min_age": 40,
                "max_age": 70,
                "diabetes_type": "Type 2"
            }
        }
