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