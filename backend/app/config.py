import os
from pydantic_settings import BaseSettings
from datetime import timedelta

class Settings(BaseSettings):
    app_name: str = "Diabetic Ulcer Detection API"
    debug: bool = os.getenv("DEBUG", "False") == "True"
    
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    cloudinary_cloud_name: str = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    cloudinary_api_key: str = os.getenv("CLOUDINARY_API_KEY", "")
    cloudinary_api_secret: str = os.getenv("CLOUDINARY_API_SECRET", "")
    
    model_path: str = os.getenv("MODEL_PATH", "./models/cnn_ulcer_model.pth")
    
    allowed_image_extensions: list = [".jpg", ".jpeg", ".png", ".bmp"]
    max_image_size_mb: int = 10
    
    class Config:
        env_file = ".env"

settings = Settings()
