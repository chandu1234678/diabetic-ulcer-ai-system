"""Application settings and configuration."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App configuration
    app_name: str = "Diabetic Ulcer AI System"
    app_version: str = "1.0.0"
    log_level: str = "INFO"
    
    # Database
    database_url: str = "postgresql://localhost:5432/diabetic_ulcer_db"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: list = ["http://localhost:3000", "http://localhost:8000"]
    
    # Model paths
    cnn_model_path: str = "../model_weights/cnn_ulcer_model.pth"
    segmentation_model_path: str = "../model_weights/segmentation_model.pth"
    multimodal_model_path: str = "../model_weights/multimodal_model.pth"
    
    # Explainability settings
    shap_background_samples: int = 100
    lime_samples: int = 1000
    gradcam_layer: str = "layer4"
    
    # Monitoring
    prometheus_port: int = 9090
    grafana_port: int = 3001
    
    # MLflow
    mlflow_tracking_uri: str = "http://localhost:5000"
    mlflow_experiment_name: str = "diabetic-ulcer-detection"
    
    # Feature toggles
    enable_explainability: bool = True
    enable_multimodal: bool = True
    enable_background_tasks: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
