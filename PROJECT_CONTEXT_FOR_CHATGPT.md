# Diabetic Ulcer AI System - Complete Project Context

## PROJECT OVERVIEW
A comprehensive AI-powered diagnostic system for detecting and analyzing diabetic ulcers. Uses CNN (ResNet50), U-Net segmentation, and multimodal learning (image + clinical data fusion). Built with FastAPI backend + React frontend. Includes explainability (SHAP, Grad-CAM, LIME), patient progression tracking, report generation, and Prometheus monitoring.

## TECH STACK
- **Backend**: FastAPI, Python 3.11, SQLAlchemy, PyTorch, Pydantic
- **Frontend**: React 19, React Router, Tailwind CSS, Chart.js
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **ML**: PyTorch (ResNet50 CNN, U-Net segmentation, Multimodal fusion)
- **Explainability**: SHAP, Grad-CAM, LIME
- **Auth**: JWT (python-jose), bcrypt (passlib)
- **Image Storage**: Cloudinary
- **Monitoring**: Prometheus + Grafana
- **Deployment**: Docker, Kubernetes, Nginx

---

## PROJECT STRUCTURE
```
hackathon/
├── docker-compose.yml
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py                    # FastAPI entry point
│       ├── config.py                  # App settings (Pydantic)
│       ├── database.py                # SQLAlchemy setup
│       ├── models.py                  # DB models (User, Patient, PredictionLog, UlcerImage)
│       ├── schemas.py                 # Pydantic schemas
│       ├── auth/
│       │   ├── auth_router.py         # /auth/register, /auth/login
│       │   ├── jwt_handler.py         # JWT create/decode
│       │   ├── dependencies.py        # get_current_user dependency
│       │   └── password_utils.py      # bcrypt hash/verify
│       ├── routes/
│       │   ├── health.py              # GET /health
│       │   ├── predict.py             # POST /predict
│       │   ├── upload.py              # POST /images/upload
│       │   ├── reports.py             # GET /reports/predictions
│       │   ├── patients.py            # CRUD /patients
│       │   └── patient_progression.py # Timeline, progression, upload-image
│       ├── services/
│       │   ├── inference_service.py   # Main inference pipeline
│       │   ├── model_loader.py        # Singleton model loading
│       │   ├── image_service.py       # Image upload/validation
│       │   ├── patient_service.py     # Patient CRUD
│       │   ├── progression_service.py # Ulcer progression analysis
│       │   ├── report_service.py      # Prediction reports
│       │   ├── clinical_data_service.py # Clinical data + risk scoring
│       │   └── ml_service.py          # Simple text prediction fallback
│       ├── ml/
│       │   ├── cnn_model.py           # UlcerCNNModel (ResNet50, 2-class)
│       │   ├── multimodal_model.py    # MultimodalUlcerModel (image+clinical)
│       │   ├── preprocess.py          # Image & clinical data preprocessing
│       │   ├── train.py               # Training loop
│       │   ├── dataset_loader.py      # UlcerDataset + DataLoader
│       │   └── ulcer_area_estimator.py # HSV-based area estimation
│       ├── models/
│       │   ├── cnn_ulcer_model.py     # CNNUlcerModel (ResNet50, 3-class)
│       │   ├── multimodal_model.py    # MultimodalModel (3-class)
│       │   ├── segmentation_model.py  # U-Net segmentation
│       │   └── load_model.py          # ModelLoader singleton
│       ├── explainability/
│       │   ├── gradcam.py             # GradCAM heatmap generation
│       │   ├── shap_explainer.py      # SHAP clinical feature importance
│       │   ├── lime_explainer.py      # LIME placeholder
│       │   └── feature_importance.py  # Permutation, gradient, integrated gradients
│       ├── monitoring/
│       │   └── metrics.py             # Prometheus counters/histograms
│       ├── utils/
│       │   ├── cloud_storage.py       # Cloudinary upload/delete
│       │   ├── validators.py          # Image/clinical data validation
│       │   ├── image_processing.py    # CLAHE, blur, edge detection
│       │   ├── helpers.py             # Data/Math/String/Time helpers
│       │   └── metrics.py             # accuracy/precision/recall
│       ├── core/
│       │   ├── config.py              # Alternative settings
│       │   ├── settings.py            # Full settings with env
│       │   ├── security.py            # Empty
│       │   └── logger.py              # Rotating file + console logger
│       └── chatbot/                   # Empty folder
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── src/
│       ├── App.jsx / App.js           # Router: Login, Register, Dashboard
│       ├── main.jsx / index.js        # React root
│       ├── App.css / index.css
│       ├── components/
│       │   ├── Login.jsx              # Login form + JWT storage
│       │   ├── Register.jsx           # Register form
│       │   ├── ImageUploader.jsx      # Drag & drop image upload
│       │   ├── ClinicalDataForm.jsx   # Patient clinical data form
│       │   ├── PredictionResult.jsx   # Analysis results display
│       │   ├── GradCamViewer.jsx      # GradCAM heatmap overlay
│       │   ├── HeatmapViewer.jsx      # Side-by-side heatmap view
│       │   ├── ShapChart.jsx          # Chart.js SHAP bar chart
│       │   ├── PatientHistory.jsx     # Patient timeline
│       │   └── LoadingSpinner.jsx     # Loading animation
│       ├── pages/
│       │   ├── Dashboard.jsx          # Overview/Analytics/Patients tabs
│       │   ├── Home.jsx               # Landing page
│       │   ├── Prediction.jsx         # Upload + predict workflow
│       │   └── Reports.jsx            # Report table + filters
│       ├── services/
│       │   ├── api_service.js         # APIService class with fetchWithAuth
│       │   └── auth.js                # register/login/logout/getToken
│       ├── store/
│       │   └── predictionStore.js     # Simple state management
│       └── styles/
│           └── dashboard.css          # Full dashboard CSS
├── datasets/
│   ├── clinical_data/patient_data.csv
│   ├── images/normal/ & images/ulcers/
│   └── segmentation_masks/
├── deployment/
│   ├── docker-compose.yml
│   ├── kubernetes/ (backend + frontend deployments)
│   ├── monitoring/ (prometheus.yml, grafana-dashboard.json)
│   └── nginx/nginx.conf
├── docs/
│   ├── api_documentation.md
│   ├── architecture.md
│   └── model_documentation.md
├── model_weights/
├── notebooks/ (cnn, multimodal, segmentation, explainability)
├── scripts/ (train, evaluate, generate_shap)
└── mlops/ (dvc.yaml, mlflow_config.yaml, model_registry)
```

---

## KEY FILES CONTENT

### backend/app/main.py
```python
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from app.database import Base, engine
from app.config import settings
from app.auth.auth_router import router as auth_router
from app.routes import health, predict, upload, reports, patients, patient_progression
from app import models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Diabetic Ulcer Detection API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.include_router(auth_router)
app.include_router(health.router)
app.include_router(predict.router)
app.include_router(upload.router)
app.include_router(reports.router)
app.include_router(patients.router)
app.include_router(patient_progression.router)

@app.get("/")
def root():
    return {"message": "Diabetic Ulcer Detection API running", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### backend/app/config.py
```python
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
```

### backend/app/database.py
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### backend/app/models.py
```python
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    patients = relationship("Patient", back_populates="user")
    prediction_logs = relationship("PredictionLog", back_populates="user")

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    patient_identifier = Column(String, unique=True, index=True)
    age = Column(Integer)
    bmi = Column(Float)
    diabetes_duration = Column(Integer)
    infection_signs = Column(String, default="none")
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="patients")
    ulcer_images = relationship("UlcerImage", back_populates="patient")
    prediction_logs = relationship("PredictionLog", back_populates="patient")

class PredictionLog(Base):
    __tablename__ = "prediction_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True)
    prediction = Column(String)
    confidence = Column(Float)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="prediction_logs")
    patient = relationship("Patient", back_populates="prediction_logs")

class UlcerImage(Base):
    __tablename__ = "ulcer_images"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    image_url = Column(String)
    prediction = Column(String)
    confidence = Column(Float)
    ulcer_area = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    patient = relationship("Patient", back_populates="ulcer_images")
```

### backend/app/schemas.py
```python
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
```

### backend/app/auth/auth_router.py
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, TokenResponse
from app.auth.password_utils import hash_password, verify_password
from app.auth.jwt_handler import create_access_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
```

### backend/app/auth/jwt_handler.py
```python
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.config import settings
from typing import Optional

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        email: str = payload.get("sub")
        return email if email else None
    except JWTError:
        return None
```

### backend/app/auth/dependencies.py
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth.jwt_handler import decode_token

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    email = decode_token(token)
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
```

### backend/app/auth/password_utils.py
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

### backend/app/routes/predict.py
```python
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
    save_prediction_log(db=db, user_id=user.id, patient_id=request.patient_id, prediction=result["prediction"], confidence=result["confidence"], image_url=request.image_url)
    return PredictionResponse(prediction=result["prediction"], confidence=result["confidence"], gradcam_heatmap=result["gradcam_heatmap"], shap_importance=result["shap_importance"], image_url=result["image_url"])
```

### backend/app/routes/patients.py
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import PatientCreate, PatientResponse
from app.services.patient_service import create_patient, get_user_patients, get_patient, delete_patient
from app.auth.dependencies import get_current_user
from app.models import User

router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("/", response_model=PatientResponse)
def create_patient_endpoint(patient: PatientCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_patient(db=db, user_id=user.id, patient=patient)

@router.get("/")
def list_patients(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user_patients(db=db, user_id=user.id)

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient_endpoint(patient_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    patient = get_patient(db=db, patient_id=patient_id)
    if patient and patient.user_id == user.id:
        return patient
    return {"error": "Patient not found"}

@router.delete("/{patient_id}")
def delete_patient_endpoint(patient_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    patient = get_patient(db=db, patient_id=patient_id)
    if patient and patient.user_id == user.id:
        delete_patient(db=db, patient_id=patient_id)
        return {"message": "Patient deleted"}
    return {"error": "Patient not found"}
```

### backend/app/routes/patient_progression.py
```python
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.progression_service import analyze_progression, add_ulcer_image, get_patient_timeline
from app.services.image_service import upload_image
from app.services.inference_service import run_inference
from app.auth.dependencies import get_current_user
from app.models import User
from app.services.patient_service import get_patient

router = APIRouter(prefix="/patients", tags=["progression"])

@router.post("/{patient_id}/upload-image")
async def upload_patient_image(patient_id: int, file: UploadFile = File(...), age: int = None, bmi: float = None, diabetes_duration: int = None, infection_signs: str = "none", user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    patient = get_patient(db=db, patient_id=patient_id)
    if not patient or patient.user_id != user.id:
        return {"error": "Patient not found"}
    image_data = await upload_image(file)
    image_url = image_data["url"]
    result = run_inference(image_url=image_url, age=age or patient.age, bmi=bmi or patient.bmi, diabetes_duration=diabetes_duration or patient.diabetes_duration, infection_signs=infection_signs or patient.infection_signs)
    ulcer_image = add_ulcer_image(db=db, patient_id=patient_id, image_url=image_url, prediction=result["prediction"], confidence=result["confidence"], ulcer_area=result["ulcer_area"])
    return {"image": ulcer_image, "prediction": result["prediction"], "confidence": result["confidence"]}

@router.get("/{patient_id}/timeline")
def get_patient_timeline_endpoint(patient_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    patient = get_patient(db=db, patient_id=patient_id)
    if not patient or patient.user_id != user.id:
        return {"error": "Patient not found"}
    return get_patient_timeline(db=db, patient_id=patient_id)

@router.get("/{patient_id}/progression")
def get_progression_endpoint(patient_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    patient = get_patient(db=db, patient_id=patient_id)
    if not patient or patient.user_id != user.id:
        return {"error": "Patient not found"}
    return analyze_progression(db=db, patient_id=patient_id)
```

### backend/app/routes/upload.py
```python
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.image_service import upload_image
from app.auth.dependencies import get_current_user
from app.models import User

router = APIRouter(prefix="/images", tags=["images"])

@router.post("/upload")
async def upload_image_endpoint(file: UploadFile = File(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return await upload_image(file)
```

### backend/app/routes/reports.py
```python
from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.report_service import generate_prediction_report
from app.auth.dependencies import get_current_user
from app.models import User

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/predictions")
def get_prediction_report(patient_id: int = Query(None), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return generate_prediction_report(db=db, user_id=user.id, patient_id=patient_id)
```

### backend/app/routes/health.py
```python
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
def health_check():
    return {"status": "healthy", "service": "diabetic_ulcer_detection_api"}
```

### backend/app/services/inference_service.py
```python
import torch
import numpy as np
from app.services.model_loader import get_model
from app.ml.preprocess import preprocess_image, preprocess_clinical_data
from app.ml.ulcer_area_estimator import estimate_ulcer_area
from app.explainability.gradcam import generate_gradcam
from app.explainability.shap_explainer import generate_shap_values
import time

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
    gradcam_heatmap = generate_gradcam(cnn_model, image_tensor)
    feature_names = ["Age", "BMI", "Diabetes Duration", "Infection Signs"]
    shap_importance = generate_shap_values(multimodal_model, clinical_tensor.cpu().numpy(), feature_names)
    ulcer_area = estimate_ulcer_area(image_url)
    inference_time = time.time() - start_time
    return {
        "prediction": prediction, "confidence": confidence, "gradcam_heatmap": gradcam_heatmap,
        "shap_importance": shap_importance, "image_url": image_url, "ulcer_area": ulcer_area,
        "inference_time": inference_time
    }
```

### backend/app/services/model_loader.py
```python
import torch
import os
from app.ml.cnn_model import create_model
from app.ml.multimodal_model import create_multimodal_model
from app.config import settings

_cnn_model = None
_multimodal_model = None

def load_cnn_model():
    global _cnn_model
    if _cnn_model is not None:
        return _cnn_model
    model = create_model(num_classes=2, pretrained=True)
    if os.path.exists(settings.model_path):
        try:
            checkpoint = torch.load(settings.model_path, map_location='cpu')
            model.load_state_dict(checkpoint)
        except:
            print(f"Could not load checkpoint from {settings.model_path}, using pretrained")
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    model.eval()
    _cnn_model = model
    return model

def load_multimodal_model():
    global _multimodal_model
    if _multimodal_model is not None:
        return _multimodal_model
    model = create_multimodal_model(image_feature_dim=2048, num_clinical_features=4, num_classes=2)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    model.eval()
    _multimodal_model = model
    return model

def get_model(model_type: str = "cnn"):
    if model_type == "cnn":
        return load_cnn_model()
    elif model_type == "multimodal":
        return load_multimodal_model()
    return load_cnn_model()
```

### backend/app/services/image_service.py
```python
from fastapi import UploadFile, HTTPException
from app.utils.cloud_storage import upload_image_to_cloud, delete_image_from_cloud
from app.utils.validators import validate_image_extension, validate_image_size
import uuid

async def upload_image(file: UploadFile):
    if not validate_image_extension(file.filename):
        raise HTTPException(status_code=400, detail="Invalid image format")
    file_content = await file.read()
    if not validate_image_size(len(file_content)):
        raise HTTPException(status_code=413, detail="File too large")
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    image_url = upload_image_to_cloud(file_content, unique_filename)
    return {"filename": unique_filename, "url": image_url, "size": len(file_content)}
```

### backend/app/services/patient_service.py
```python
from sqlalchemy.orm import Session
from app.models import Patient
from app.schemas import PatientCreate

def create_patient(db: Session, user_id: int, patient: PatientCreate):
    db_patient = Patient(user_id=user_id, patient_identifier=patient.patient_identifier, age=patient.age, bmi=patient.bmi, diabetes_duration=patient.diabetes_duration, infection_signs=patient.infection_signs)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patient(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()

def get_user_patients(db: Session, user_id: int):
    return db.query(Patient).filter(Patient.user_id == user_id).all()

def delete_patient(db: Session, patient_id: int):
    patient = get_patient(db, patient_id)
    if patient:
        db.delete(patient)
        db.commit()
    return patient
```

### backend/app/services/progression_service.py
```python
from sqlalchemy.orm import Session
from app.models import UlcerImage
from app.schemas import PatientProgressionResponse

def get_patient_timeline(db: Session, patient_id: int):
    return db.query(UlcerImage).filter(UlcerImage.patient_id == patient_id).order_by(UlcerImage.created_at).all()

def analyze_progression(db: Session, patient_id: int):
    images = get_patient_timeline(db, patient_id)
    if len(images) < 2:
        return PatientProgressionResponse(trend="insufficient_data", previous_area=0.0, latest_area=0.0, percentage_change=0.0, total_images=len(images))
    previous_area = images[-2].ulcer_area
    latest_area = images[-1].ulcer_area
    percentage_change = ((latest_area - previous_area) / previous_area) * 100 if previous_area != 0 else 0
    trend = "healing" if percentage_change < -5 else ("worsening" if percentage_change > 5 else "stable")
    return PatientProgressionResponse(trend=trend, previous_area=previous_area, latest_area=latest_area, percentage_change=percentage_change, total_images=len(images))

def add_ulcer_image(db: Session, patient_id: int, image_url: str, prediction: str, confidence: float, ulcer_area: float):
    ulcer_image = UlcerImage(patient_id=patient_id, image_url=image_url, prediction=prediction, confidence=confidence, ulcer_area=ulcer_area)
    db.add(ulcer_image)
    db.commit()
    db.refresh(ulcer_image)
    return ulcer_image
```

### backend/app/services/report_service.py
```python
from sqlalchemy.orm import Session
from app.models import PredictionLog
from datetime import datetime

def generate_prediction_report(db: Session, user_id: int, patient_id: int = None):
    query = db.query(PredictionLog).filter(PredictionLog.user_id == user_id)
    if patient_id:
        query = query.filter(PredictionLog.patient_id == patient_id)
    logs = query.all()
    total_predictions = len(logs)
    ulcer_predictions = sum(1 for log in logs if log.prediction == "ulcer")
    normal_predictions = sum(1 for log in logs if log.prediction == "normal")
    avg_confidence = sum(log.confidence for log in logs) / len(logs) if logs else 0
    return {
        "total_predictions": total_predictions, "ulcer_predictions": ulcer_predictions,
        "normal_predictions": normal_predictions, "average_confidence": avg_confidence,
        "ulcer_percentage": (ulcer_predictions / total_predictions * 100) if total_predictions > 0 else 0,
        "report_generated_at": datetime.utcnow()
    }

def save_prediction_log(db: Session, user_id: int, patient_id: int = None, prediction: str = "", confidence: float = 0, image_url: str = ""):
    log = PredictionLog(user_id=user_id, patient_id=patient_id, prediction=prediction, confidence=confidence, image_url=image_url)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
```

### backend/app/ml/cnn_model.py
```python
import torch
import torch.nn as nn
import torchvision.models as models

class UlcerCNNModel(nn.Module):
    def __init__(self, num_classes=2, pretrained=True):
        super(UlcerCNNModel, self).__init__()
        self.resnet = models.resnet50(pretrained=pretrained)
        num_ftrs = self.resnet.fc.in_features
        self.resnet.fc = nn.Linear(num_ftrs, num_classes)

    def forward(self, x):
        return self.resnet(x)

    def get_features(self, x):
        x = self.resnet.conv1(x)
        x = self.resnet.bn1(x)
        x = self.resnet.relu(x)
        x = self.resnet.maxpool(x)
        x = self.resnet.layer1(x)
        x = self.resnet.layer2(x)
        x = self.resnet.layer3(x)
        x = self.resnet.layer4(x)
        x = self.resnet.avgpool(x)
        return torch.flatten(x, 1)

def create_model(num_classes=2, pretrained=True):
    return UlcerCNNModel(num_classes=num_classes, pretrained=pretrained)
```

### backend/app/ml/multimodal_model.py
```python
import torch
import torch.nn as nn

class MultimodalUlcerModel(nn.Module):
    def __init__(self, image_feature_dim=2048, num_clinical_features=4, num_classes=2):
        super(MultimodalUlcerModel, self).__init__()
        self.image_fc = nn.Sequential(nn.Linear(image_feature_dim, 512), nn.ReLU(), nn.Dropout(0.3))
        self.clinical_fc = nn.Sequential(nn.Linear(num_clinical_features, 64), nn.ReLU(), nn.Dropout(0.3))
        self.fusion_fc = nn.Sequential(nn.Linear(512 + 64, 256), nn.ReLU(), nn.Dropout(0.3), nn.Linear(256, 128), nn.ReLU(), nn.Dropout(0.3), nn.Linear(128, num_classes))

    def forward(self, image_features, clinical_features):
        x_image = self.image_fc(image_features)
        x_clinical = self.clinical_fc(clinical_features)
        x = torch.cat([x_image, x_clinical], dim=1)
        return self.fusion_fc(x)

def create_multimodal_model(image_feature_dim=2048, num_clinical_features=4, num_classes=2):
    return MultimodalUlcerModel(image_feature_dim, num_clinical_features, num_classes)
```

### backend/app/ml/preprocess.py
```python
import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import io
import requests

def get_preprocessing_transforms():
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

def download_image(image_url: str) -> Image.Image:
    response = requests.get(image_url, timeout=10)
    response.raise_for_status()
    return Image.open(io.BytesIO(response.content)).convert('RGB')

def preprocess_image(image_path_or_url: str) -> torch.Tensor:
    if image_path_or_url.startswith(('http://', 'https://')):
        image = download_image(image_path_or_url)
    else:
        image = Image.open(image_path_or_url).convert('RGB')
    return get_preprocessing_transforms()(image).unsqueeze(0)

def preprocess_clinical_data(age: int, bmi: float, diabetes_duration: int, infection_signs: str) -> torch.Tensor:
    infection_map = {"none": 0.0, "mild": 0.33, "moderate": 0.66, "severe": 1.0}
    infection_value = infection_map.get(infection_signs.lower(), 0.0)
    return torch.tensor([[age / 100.0, bmi / 50.0, diabetes_duration / 50.0, infection_value]], dtype=torch.float32)
```

### backend/app/explainability/gradcam.py
```python
import torch
import torch.nn.functional as F
import numpy as np
import cv2

class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        self.target_layer.register_forward_hook(self.save_activations)
        self.target_layer.register_full_backward_hook(self.save_gradients)

    def save_activations(self, module, input, output):
        self.activations = output.detach()

    def save_gradients(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()

    def generate_heatmap(self, input_tensor, target_class=None):
        self.model.eval()
        with torch.enable_grad():
            input_tensor.requires_grad_(True)
            output = self.model(input_tensor)
            if target_class is None:
                target_class = output.argmax(dim=1).item()
            self.model.zero_grad()
            score = output[0, target_class]
            score.backward()
        pooled_gradients = torch.mean(self.gradients, dim=[0, 2, 3])
        activations = self.activations[0]
        for i in range(activations.shape[0]):
            activations[i, :, :] *= pooled_gradients[i]
        heatmap = torch.mean(activations, dim=0).cpu().numpy()
        heatmap = np.maximum(heatmap, 0)
        heatmap /= (heatmap.max() + 1e-8)
        heatmap_resized = cv2.resize(heatmap, (224, 224))
        return np.uint8(255 * heatmap_resized).tolist()

def generate_gradcam(model, input_tensor, target_layer=None):
    if target_layer is None:
        target_layer = model.resnet.layer4[-1]
    return GradCAM(model, target_layer).generate_heatmap(input_tensor)
```

### backend/app/explainability/shap_explainer.py
```python
import numpy as np
import shap
import torch

class ShapExplainer:
    def __init__(self, model, background_data=None, num_background_samples=100):
        self.model = model
        self.num_background_samples = num_background_samples

    def explain_clinical_features(self, clinical_data, feature_names):
        explainer = shap.KernelExplainer(self._predict_fn, np.random.randn(self.num_background_samples, clinical_data.shape[1]))
        shap_values = explainer.shap_values(clinical_data)
        if isinstance(shap_values, list):
            shap_values = shap_values[1]
        return {name: float(np.abs(shap_values[0, i])) for i, name in enumerate(feature_names)}

    def _predict_fn(self, X):
        X_tensor = torch.from_numpy(X).float()
        with torch.no_grad():
            predictions = self.model(X_tensor)
            if len(predictions.shape) > 1:
                return torch.softmax(predictions, dim=1)[:, 1].numpy()
            return predictions.numpy()

def generate_shap_values(model, clinical_features, feature_names):
    return ShapExplainer(model).explain_clinical_features(clinical_features, feature_names)
```

### backend/app/ml/ulcer_area_estimator.py
```python
import numpy as np
from PIL import Image
import requests
import io

def estimate_ulcer_area(image_url: str) -> float:
    response = requests.get(image_url, timeout=10)
    response.raise_for_status()
    image = Image.open(io.BytesIO(response.content)).convert('RGB')
    image_array = np.array(image)
    hsv_image = Image.fromarray(image_array.astype('uint8')).convert('HSV')
    hsv_array = np.array(hsv_image)
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([30, 255, 255])
    mask = np.all((hsv_array >= lower_red) & (hsv_array <= upper_red), axis=2)
    ulcer_pixels = np.sum(mask)
    total_pixels = image_array.shape[0] * image_array.shape[1]
    return min(ulcer_pixels / total_pixels, 1.0)
```

### backend/app/utils/cloud_storage.py
```python
import cloudinary
import cloudinary.uploader
from app.config import settings

cloudinary.config(cloud_name=settings.cloudinary_cloud_name, api_key=settings.cloudinary_api_key, api_secret=settings.cloudinary_api_secret)

def upload_image_to_cloud(file_content: bytes, filename: str) -> str:
    if not settings.cloudinary_cloud_name:
        return f"local://{filename}"
    try:
        result = cloudinary.uploader.upload(file_content, public_id=filename, folder="ulcer_images", resource_type="auto")
        return result.get("secure_url", result.get("url"))
    except Exception as e:
        return f"local://{filename}"

def delete_image_from_cloud(public_id: str) -> bool:
    if not settings.cloudinary_cloud_name:
        return True
    try:
        result = cloudinary.uploader.destroy(f"ulcer_images/{public_id}")
        return result.get("result") == "ok"
    except:
        return False
```

### backend/app/utils/validators.py
```python
from app.config import settings
import os

def validate_image_extension(filename: str) -> bool:
    _, ext = os.path.splitext(filename.lower())
    return ext in settings.allowed_image_extensions

def validate_image_size(file_size_bytes: int) -> bool:
    return file_size_bytes <= settings.max_image_size_mb * 1024 * 1024

def validate_clinical_data(age: int, bmi: float, diabetes_duration: int) -> bool:
    if age < 0 or age > 150: return False
    if bmi < 10 or bmi > 60: return False
    if diabetes_duration < 0 or diabetes_duration > 100: return False
    return True

def validate_infection_signs(infection_signs: str) -> bool:
    return infection_signs.lower() in ["none", "mild", "moderate", "severe"]
```

### backend/app/monitoring/metrics.py
```python
from prometheus_client import Counter, Histogram, Gauge

predictions_total = Counter('predictions_total', 'Total number of predictions', ['model'])
prediction_latency = Histogram('prediction_latency_seconds', 'Prediction latency in seconds', ['model'])
model_inference_time = Histogram('model_inference_seconds', 'Model inference time in seconds', ['model'])
active_requests = Gauge('active_requests_total', 'Number of active requests')

def track_prediction(model_name: str):
    predictions_total.labels(model=model_name).inc()

def track_inference_time(model_name: str, duration: float):
    model_inference_time.labels(model=model_name).observe(duration)
    prediction_latency.labels(model=model_name).observe(duration)
```

### backend/app/models/cnn_ulcer_model.py (3-class version)
```python
import torch
import torch.nn as nn
from torchvision import models

class CNNUlcerModel(nn.Module):
    def __init__(self, num_classes=3, pretrained=True):
        super(CNNUlcerModel, self).__init__()
        self.backbone = models.resnet50(pretrained=pretrained)
        num_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Sequential(
            nn.Dropout(0.5), nn.Linear(num_features, 512), nn.ReLU(inplace=True),
            nn.Dropout(0.3), nn.Linear(512, 256), nn.ReLU(inplace=True), nn.Linear(256, num_classes)
        )

    def forward(self, x):
        return self.backbone(x)

def create_cnn_model(num_classes=3, pretrained=True):
    return CNNUlcerModel(num_classes=num_classes, pretrained=pretrained)
```

### backend/app/models/segmentation_model.py
```python
import torch
import torch.nn as nn

class SegmentationModel(nn.Module):
    def __init__(self, num_classes=2):
        super(SegmentationModel, self).__init__()
        self.encoder = nn.Sequential(nn.Conv2d(3, 64, 3, padding=1), nn.ReLU(), nn.Conv2d(64, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2, 2))
        self.decoder = nn.Sequential(nn.ConvTranspose2d(64, 64, 2, stride=2), nn.ReLU(), nn.Conv2d(64, num_classes, 1))

    def forward(self, x):
        return self.decoder(self.encoder(x))

def create_segmentation_model(num_classes=2):
    return SegmentationModel(num_classes=num_classes)
```

---

## FRONTEND FILES

### frontend/src/App.jsx
```jsx
import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Login from './components/Login'
import Register from './components/Register'
import Dashboard from './pages/Dashboard'
import './App.css'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    setIsAuthenticated(!!token)
    setLoading(false)
  }, [])

  if (loading) return <div className="flex items-center justify-center h-screen">Loading...</div>

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login onLogin={() => setIsAuthenticated(true)} />} />
        <Route path="/register" element={<Register onRegister={() => setIsAuthenticated(true)} />} />
        <Route path="/dashboard" element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />} />
        <Route path="/" element={isAuthenticated ? <Navigate to="/dashboard" /> : <Navigate to="/login" />} />
      </Routes>
    </Router>
  )
}

export default App
```

### frontend/src/services/api_service.js
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class APIService {
  async fetchWithAuth(endpoint, options = {}) {
    const token = localStorage.getItem('access_token');
    const headers = { 'Content-Type': 'application/json', ...options.headers };
    if (token) headers['Authorization'] = `Bearer ${token}`;
    const response = await fetch(`${API_BASE_URL}${endpoint}`, { ...options, headers });
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `API Error: ${response.status}`);
    }
    return response.json();
  }

  async healthCheck() { return this.fetchWithAuth('/health'); }

  async predict(imageUrl, clinicalData) {
    return this.fetchWithAuth('/predict', {
      method: 'POST',
      body: JSON.stringify({ image_url: imageUrl, age: clinicalData.age, bmi: clinicalData.bmi, diabetes_duration: clinicalData.diabetes_duration, infection_signs: clinicalData.infection_signs })
    });
  }

  async uploadImage(file) {
    const formData = new FormData();
    formData.append('file', file);
    const token = localStorage.getItem('access_token');
    const headers = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;
    const response = await fetch(`${API_BASE_URL}/images/upload`, { method: 'POST', headers, body: formData });
    if (!response.ok) throw new Error('Image upload failed');
    return response.json();
  }

  async getPatientTimeline(patientId) { return this.fetchWithAuth(`/patients/${patientId}/timeline`); }
  async getPatientProgression(patientId) { return this.fetchWithAuth(`/patients/${patientId}/progression`); }

  async uploadPatientImage(patientId, file) {
    const formData = new FormData();
    formData.append('file', file);
    const token = localStorage.getItem('access_token');
    const headers = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;
    const response = await fetch(`${API_BASE_URL}/patients/${patientId}/upload-image`, { method: 'POST', headers, body: formData });
    if (!response.ok) throw new Error('Patient image upload failed');
    return response.json();
  }

  async generateReport(predictionId) { return this.fetchWithAuth(`/reports/${predictionId}`, { method: 'POST' }); }
}

const apiService = new APIService();
export default apiService;
export async function getPatientTimeline(patientId) { return apiService.getPatientTimeline(patientId); }
```

### frontend/src/services/auth.js
```javascript
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000'

export async function registerUser(email, password) {
  const response = await fetch(`${API_BASE}/auth/register`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password }) })
  if (!response.ok) { const error = await response.json(); throw new Error(error.detail || 'Registration failed') }
  return response.json()
}

export async function loginUser(email, password) {
  const response = await fetch(`${API_BASE}/auth/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password }) })
  if (!response.ok) { const error = await response.json(); throw new Error(error.detail || 'Login failed') }
  return response.json()
}

export function logout() { localStorage.removeItem('access_token') }
export function getToken() { return localStorage.getItem('access_token') }
export function isAuthenticated() { return !!getToken() }
```

### frontend/src/components/Login.jsx
```jsx
import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { loginUser } from '../services/auth'

export default function Login({ onLogin }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true); setError('')
    try {
      const response = await loginUser(email, password)
      localStorage.setItem('access_token', response.access_token)
      onLogin(); navigate('/dashboard')
    } catch (err) { setError(err.message || 'Login failed') }
    finally { setLoading(false) }
  }

  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-600 to-purple-600 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-xl p-8 w-full max-w-md">
        <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">Login</h1>
        {error && <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="mb-4"><label className="block text-gray-700 font-semibold mb-2">Email</label><input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
          <div className="mb-6"><label className="block text-gray-700 font-semibold mb-2">Password</label><input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
          <button type="submit" disabled={loading} className="w-full bg-blue-600 text-white font-semibold py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50">{loading ? 'Logging in...' : 'Login'}</button>
        </form>
        <p className="text-gray-600 text-center mt-4">Don't have an account? <Link to="/register" className="text-blue-600 hover:underline">Register here</Link></p>
      </div>
    </div>
  )
}
```

### frontend/src/components/Register.jsx
```jsx
import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { registerUser } from '../services/auth'

export default function Register({ onRegister }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault(); setError('')
    if (password !== confirmPassword) { setError('Passwords do not match'); return }
    setLoading(true)
    try {
      const response = await registerUser(email, password)
      localStorage.setItem('access_token', response.access_token)
      onRegister(); navigate('/dashboard')
    } catch (err) { setError(err.message || 'Registration failed') }
    finally { setLoading(false) }
  }

  return (
    <div className="min-h-screen bg-gradient-to-r from-green-600 to-blue-600 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-xl p-8 w-full max-w-md">
        <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">Register</h1>
        {error && <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="mb-4"><label className="block text-gray-700 font-semibold mb-2">Email</label><input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="w-full px-4 py-2 border rounded-lg" required /></div>
          <div className="mb-4"><label className="block text-gray-700 font-semibold mb-2">Password</label><input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="w-full px-4 py-2 border rounded-lg" required /></div>
          <div className="mb-6"><label className="block text-gray-700 font-semibold mb-2">Confirm Password</label><input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} className="w-full px-4 py-2 border rounded-lg" required /></div>
          <button type="submit" disabled={loading} className="w-full bg-green-600 text-white font-semibold py-2 rounded-lg hover:bg-green-700 disabled:opacity-50">{loading ? 'Creating account...' : 'Register'}</button>
        </form>
        <p className="text-gray-600 text-center mt-4">Already have an account? <Link to="/login" className="text-green-600 hover:underline">Login here</Link></p>
      </div>
    </div>
  )
}
```

### frontend/src/pages/Dashboard.jsx
```jsx
import React, { useState } from 'react';
import '../styles/dashboard.css';

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  return (
    <div className="dashboard-container">
      <div className="dashboard-header"><h1>Clinical Dashboard</h1><div className="date-range-selector"><input type="date" /><input type="date" /></div></div>
      <div className="dashboard-tabs">
        <button className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`} onClick={() => setActiveTab('overview')}>Overview</button>
        <button className={`tab-btn ${activeTab === 'analytics' ? 'active' : ''}`} onClick={() => setActiveTab('analytics')}>Analytics</button>
        <button className={`tab-btn ${activeTab === 'patients' ? 'active' : ''}`} onClick={() => setActiveTab('patients')}>Patients</button>
      </div>
      <div className="dashboard-content">
        {activeTab === 'overview' && (<div className="overview-section"><div className="stats-grid">
          <div className="stat-card"><h3>Total Patients</h3><p className="stat-value">1,234</p></div>
          <div className="stat-card"><h3>Ulcers Detected</h3><p className="stat-value">156</p></div>
          <div className="stat-card"><h3>Success Rate</h3><p className="stat-value">94.2%</p></div>
          <div className="stat-card"><h3>Avg Response Time</h3><p className="stat-value">1.2s</p></div>
        </div></div>)}
        {activeTab === 'analytics' && (<div className="analytics-section"><h2>System Analytics</h2></div>)}
        {activeTab === 'patients' && (<div className="patients-section"><h2>Patient List</h2></div>)}
      </div>
    </div>
  );
}
```

---

## API ENDPOINTS SUMMARY
| Method | Route | Auth | Description |
|--------|-------|------|-------------|
| POST | /auth/register | No | Register user, returns JWT |
| POST | /auth/login | No | Login user, returns JWT |
| GET | /health/ | No | Health check |
| GET | / | No | Root endpoint |
| POST | /predict/ | Yes | Run ML prediction (image+clinical) |
| POST | /images/upload | Yes | Upload image to Cloudinary |
| GET | /reports/predictions | Yes | Get prediction report |
| POST | /patients/ | Yes | Create patient |
| GET | /patients/ | Yes | List user's patients |
| GET | /patients/{id} | Yes | Get patient |
| DELETE | /patients/{id} | Yes | Delete patient |
| POST | /patients/{id}/upload-image | Yes | Upload + predict patient image |
| GET | /patients/{id}/timeline | Yes | Get patient timeline |
| GET | /patients/{id}/progression | Yes | Get ulcer progression analysis |
| GET | /metrics | No | Prometheus metrics |

## DB MODELS
- **User**: id, email, hashed_password, is_active, created_at → has patients, prediction_logs
- **Patient**: id, user_id(FK), patient_identifier, age, bmi, diabetes_duration, infection_signs, created_at → has ulcer_images, prediction_logs
- **PredictionLog**: id, user_id(FK), patient_id(FK), prediction, confidence, image_url, created_at
- **UlcerImage**: id, patient_id(FK), image_url, prediction, confidence, ulcer_area, created_at

## ML PIPELINE FLOW
1. Image uploaded → Cloudinary storage
2. Image preprocessed (resize 224x224, normalize with ImageNet stats)
3. Clinical data normalized (age/100, bmi/50, duration/50, infection mapped)
4. CNN (ResNet50) extracts 2048-dim image features
5. Multimodal model fuses image features + 4 clinical features → prediction
6. GradCAM generates heatmap from ResNet50 layer4
7. SHAP explains clinical feature importance
8. Ulcer area estimated via HSV color thresholding
9. Results saved to PredictionLog table

## DOCKER
- **Backend**: Python 3.11, uvicorn on port 8000
- **Frontend**: Node 18, serve build on port 3000
- **Nginx**: Reverse proxy, /api/ → backend, / → frontend

## requirements.txt
```
fastapi==0.104.1, uvicorn==0.24.0, sqlalchemy==2.0.23, pydantic==2.5.0, pydantic-settings==2.1.0,
python-jose==3.3.0, passlib==1.7.4, bcrypt==4.1.1, python-multipart==0.0.6, pillow==10.1.0,
torch==2.1.1, torchvision==0.16.1, numpy==1.24.3, scikit-learn==1.3.2, shap==0.43.0,
opencv-python==4.8.1.78, requests==2.31.0, cloudinary==1.36.0, prometheus-client==0.19.0,
mlflow==2.10.0, python-dotenv==1.0.0, psycopg2-binary==2.9.9, fastapi-cors==0.0.6
```

## package.json (frontend)
```
react: ^19.2.4, react-dom: ^19.2.4, react-scripts: 5.0.1
Scripts: start (react-scripts start), build, test, eject
```
