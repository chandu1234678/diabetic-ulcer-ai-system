import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from prometheus_client import make_asgi_app
from backend.app.database import Base, engine
from backend.app.config import settings
from backend.app.auth.auth_router import router as auth_router
from backend.app.routes import health, predict, upload, reports, patients, patient_progression, statistics, health_metrics, diagnostics
from backend.app import models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Diabetic Ulcer Detection API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins() if settings.environment == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded images
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.include_router(auth_router)
app.include_router(health.router)
app.include_router(predict.router)
app.include_router(upload.router)
app.include_router(reports.router)
app.include_router(patients.router)
app.include_router(patient_progression.router)
app.include_router(statistics.router)
app.include_router(health_metrics.router)
app.include_router(diagnostics.router)

@app.get("/")
def root():
    return {"message": "Diabetic Ulcer Detection API running", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)