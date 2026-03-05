"""Clinical data management service."""

import logging
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, validator
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)


class ClinicalDataModel(BaseModel):
    """Schema for clinical data."""
    patient_id: str
    age: int
    gender: str
    diabetes_type: str  # Type 1 or Type 2
    duration_of_diabetes: float  # years
    hba1c_level: Optional[float] = None  # glycemic control
    bmi: Optional[float] = None
    smoking_status: Optional[str] = None
    neuropathy: Optional[bool] = None  # peripheral neuropathy
    wound_location: Optional[str] = None
    wound_size: Optional[float] = None  # in cm^2
    infection_status: Optional[bool] = None
    previous_ulcers: Optional[int] = None
    medications: Optional[List[str]] = None
    comorbidities: Optional[List[str]] = None
    
    @validator("age")
    def age_range(cls, v):
        if v < 0 or v > 150:
            raise ValueError("Age must be between 0 and 150")
        return v
    
    @validator("diabetes_type")
    def valid_diabetes_type(cls, v):
        if v not in ["Type 1", "Type 2", "Gestational", "Other"]:
            raise ValueError("Invalid diabetes type")
        return v
    
    @validator("gender")
    def valid_gender(cls, v):
        if v not in ["M", "F", "Other"]:
            raise ValueError("Invalid gender")
        return v


class ClinicalDataService:
    """
    Service for managing clinical data.
    
    Features:
    - Data validation
    - Data normalization
    - Risk scoring
    - Patient history management
    """
    
    def __init__(self):
        """Initialize clinical data service."""
        self.data_store = {}  # Simple in-memory store
    
    def store_clinical_data(self, data: ClinicalDataModel) -> bool:
        """
        Store clinical data for a patient.
        
        Args:
            data: Clinical data model
        
        Returns:
            Success status
        """
        try:
            self.data_store[data.patient_id] = {
                "data": data.dict(),
                "timestamp": datetime.now().isoformat()
            }
            logger.info(f"Stored clinical data for patient {data.patient_id}")
            return True
        except Exception as e:
            logger.error(f"Error storing clinical data: {str(e)}")
            return False
    
    def retrieve_clinical_data(
        self,
        patient_id: str
    ) -> Optional[ClinicalDataModel]:
        """
        Retrieve clinical data for a patient.
        
        Args:
            patient_id: Patient ID
        
        Returns:
            Clinical data or None
        """
        try:
            if patient_id not in self.data_store:
                logger.warning(f"No data found for patient {patient_id}")
                return None
            
            data_dict = self.data_store[patient_id]["data"]
            return ClinicalDataModel(**data_dict)
        
        except Exception as e:
            logger.error(f"Error retrieving clinical data: {str(e)}")
            return None
    
    def normalize_clinical_data(
        self,
        data: ClinicalDataModel
    ) -> Dict[str, float]:
        """
        Normalize clinical data to model input format.
        
        Args:
            data: Clinical data
        
        Returns:
            Normalized features
        """
        try:
            normalized = {
                "age_norm": data.age / 100,  # 0-1
                "bmi_norm": (data.bmi / 50) if data.bmi else 0.5,  # 0-1
                "hba1c_norm": (data.hba1c_level / 15) if data.hba1c_level else 0.5,  # 0-1
                "duration_norm": min(data.duration_of_diabetes / 50, 1.0),  # 0-1
                "neuropathy_flag": 1.0 if data.neuropathy else 0.0,
                "infection_flag": 1.0 if data.infection_status else 0.0,
                "previous_ulcers_norm": min(
                    (data.previous_ulcers or 0) / 10, 1.0
                ),  # 0-1
                "smoking_flag": 1.0 if data.smoking_status == "Active" else 0.0,
            }
            
            logger.debug(f"Normalized clinical data for patient {data.patient_id}")
            return normalized
        
        except Exception as e:
            logger.error(f"Error normalizing clinical data: {str(e)}")
            return {}
    
    def calculate_risk_score(self, data: ClinicalDataModel) -> dict:
        """
        Calculate risk score based on clinical data.
        
        Args:
            data: Clinical data
        
        Returns:
            Risk assessment dictionary
        """
        try:
            risk_factors = []
            score = 0
            
            # Age risk
            if data.age > 65:
                risk_factors.append("Advanced age")
                score += 10
            
            # Diabetes control
            if data.hba1c_level and data.hba1c_level > 8:
                risk_factors.append("Poor glycemic control")
                score += 15
            
            # Neuropathy
            if data.neuropathy:
                risk_factors.append("Peripheral neuropathy")
                score += 20
            
            # BMI
            if data.bmi and data.bmi > 30:
                risk_factors.append("Obesity")
                score += 10
            
            # Previous ulcers
            if (data.previous_ulcers or 0) > 0:
                risk_factors.append(f"{data.previous_ulcers} previous ulcers")
                score += 15
            
            # Smoking
            if data.smoking_status == "Active":
                risk_factors.append("Active smoking")
                score += 10
            
            # Infection
            if data.infection_status:
                risk_factors.append("Active infection")
                score += 25
            
            risk_level = self._classify_risk_level(score)
            
            result = {
                "total_score": min(score, 100),
                "risk_level": risk_level,
                "risk_factors": risk_factors,
                "recommendations": self._get_recommendations(risk_level),
                "monitoring_frequency": self._get_monitoring_frequency(risk_level)
            }
            
            logger.info(f"Calculated risk score for patient {data.patient_id}: {risk_level}")
            return result
        
        except Exception as e:
            logger.error(f"Error calculating risk score: {str(e)}")
            return {}
    
    def _classify_risk_level(self, score: int) -> str:
        """Classify risk level based on score."""
        if score < 20:
            return "Low"
        elif score < 40:
            return "Moderate"
        elif score < 70:
            return "High"
        else:
            return "Very High"
    
    def _get_recommendations(self, risk_level: str) -> List[str]:
        """Get recommendations based on risk level."""
        recommendations_map = {
            "Low": [
                "Continue routine foot care",
                "Annual screening recommended"
            ],
            "Moderate": [
                "Increase foot monitoring frequency",
                "Schedule 6-monthly assessments"
            ],
            "High": [
                "Intensive wound care protocol",
                "Monthly professional assessments",
                "Consider specialist referral"
            ],
            "Very High": [
                "Immediate specialist consultation",
                "Intensive care management",
                "Possible hospitalization"
            ]
        }
        
        return recommendations_map.get(risk_level, [])
    
    def _get_monitoring_frequency(self, risk_level: str) -> str:
        """Get recommended monitoring frequency."""
        frequency_map = {
            "Low": "Annually",
            "Moderate": "Every 6 months",
            "High": "Monthly",
            "Very High": "Weekly or more"
        }
        
        return frequency_map.get(risk_level, "As needed")
    
    def export_to_csv(
        self,
        output_path: str
    ) -> bool:
        """
        Export all clinical data to CSV.
        
        Args:
            output_path: Path to save CSV file
        
        Returns:
            Success status
        """
        try:
            data_list = [
                {**v["data"], "timestamp": v["timestamp"]}
                for v in self.data_store.values()
            ]
            
            df = pd.DataFrame(data_list)
            df.to_csv(output_path, index=False)
            
            logger.info(f"Exported clinical data to {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error exporting data: {str(e)}")
            return False


def create_clinical_data_service() -> ClinicalDataService:
    """Create clinical data service."""
    return ClinicalDataService()
