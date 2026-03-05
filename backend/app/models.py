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
