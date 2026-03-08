import os
from pydantic_settings import BaseSettings
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ROOT_ENV_FILE = os.path.join(BASE_DIR, ".env")

class Settings(BaseSettings):
    app_name: str = "Diabetic Ulcer Detection API"
    debug: bool = os.getenv("DEBUG", "False") == "True"
    
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    jwt_secret_key: str = os.getenv(
        "JWT_SECRET_KEY",
        os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    )
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", os.getenv("ALGORITHM", "HS256"))
    access_token_expire_minutes: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    )
    
    cloudinary_cloud_name: str = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    cloudinary_api_key: str = os.getenv("CLOUDINARY_API_KEY", "")
    cloudinary_api_secret: str = os.getenv("CLOUDINARY_API_SECRET", "")
    
    # Standard model paths
    cnn_model_path: str = os.getenv("CNN_MODEL_PATH", os.path.join(BASE_DIR, "backend", "models", "best_dfu_model.pth"))
    segmentation_model_path: str = os.getenv("SEGMENTATION_MODEL_PATH", os.path.join(BASE_DIR, "backend", "models", "segmentation_model.pth"))
    multimodal_model_path: str = os.getenv("MULTIMODAL_MODEL_PATH", os.path.join(BASE_DIR, "backend", "models", "multimodal_model.pth"))
    
    allowed_image_extensions: list = [".jpg", ".jpeg", ".png", ".bmp"]
    max_image_size_mb: int = 10
    
    # Email Configuration (SMTP)
    smtp_server: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_username: str = os.getenv("SMTP_USERNAME", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")
    smtp_from_email: str = os.getenv("SMTP_FROM_EMAIL", "noreply@diabeticulcer.com")
    smtp_from_name: str = os.getenv("SMTP_FROM_NAME", "Diabetic Ulcer AI System")
    
    # Frontend URL
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    class Config:
        env_file = (ROOT_ENV_FILE, ".env")
        extra = "ignore"  # Ignore extra fields from .env

settings = Settings()
