# Diabetic Ulcer Explainable AI Platform

## Overview

This project explores how artificial intelligence can assist clinicians in detecting and monitoring **diabetic foot ulcers**.

The goal is to build an **Explainable AI Clinical Decision Support System** that combines **medical image analysis** and **clinical data** to estimate ulcer risk and provide interpretable insights.

The platform is designed as a **full-stack AI application** consisting of:

* **React frontend** for the clinical dashboard
* **FastAPI backend** for APIs and data processing
* **Machine learning pipeline** for prediction and explainability

In addition to predictions, the system generates explanations such as **Grad-CAM heatmaps** and **SHAP feature importance visualizations**.

This project was built to explore modern technologies including **FastAPI, PyTorch, React, Docker, MLflow, and Prometheus monitoring**.

---

# Problem Statement

Diabetic foot ulcers are one of the most serious complications of diabetes. According to the **International Diabetes Federation**, millions of patients worldwide develop foot ulcers each year, which can lead to infection, hospitalization, and amputation.

Early detection and continuous monitoring are critical.

However, many AI systems behave as **black boxes**, making it difficult for clinicians to trust predictions.

This project focuses on **Explainable AI**, providing both predictions and interpretable outputs that help clinicians understand how the model reaches its decisions.

---

# Features

* Diabetic ulcer detection from foot images
* Integration of clinical data (age, BMI, diabetes duration, etc.)
* Explainable AI visualizations
* Grad-CAM heatmaps for image explanation
* SHAP feature importance for clinical data
* Patient timeline tracking and ulcer progression monitoring
* JWT-based authentication system
* Cloud image storage
* Monitoring with Prometheus and Grafana
* ML experiment tracking using MLflow

---

# System Architecture

The system follows a **modular full-stack architecture**.

**Frontend (React)** provides the clinical dashboard interface.

**Backend (FastAPI)** exposes REST APIs for:

* prediction
* authentication
* patient data management
* model inference

The **machine learning pipeline** performs:

* image preprocessing
* prediction
* explainability analysis

High-level architecture:

```
Frontend (React)
        ↓
FastAPI Backend
        ↓
AI Models (PyTorch)
        ↓
Database + Cloud Storage
```

---

# Technology Stack

## Frontend

* React
* Vite
* TailwindCSS
* Chart.js

## Backend

* FastAPI
* SQLAlchemy
* Pydantic
* JWT Authentication
* Cloudinary (image storage)

## Machine Learning

* PyTorch
* CNN for image classification
* Multimodal model combining image and clinical data
* Grad-CAM visualization
* SHAP explainability

## DevOps / MLOps

* Docker
* Prometheus monitoring
* Grafana dashboards
* MLflow experiment tracking
* DVC dataset versioning

---

# Project Structure

```
diabetic-ulcer-ai-system/

backend/
│
├── app/
│   ├── auth/
│   ├── routes/
│   ├── services/
│   ├── ml/
│   ├── explainability/
│   └── monitoring/
│
└── requirements.txt


frontend/
│
└── src/
    ├── components/
    ├── pages/
    ├── services/
    └── styles/


datasets/
│
├── images/
├── segmentation_masks/
└── clinical_data/


deployment/
│
├── monitoring/
├── nginx/
└── kubernetes/


docs/
```

---

# Getting Started

## 1. Clone the repository

```
git clone https://github.com/chandu1234678/diabetic-ulcer-ai-system.git
cd diabetic-ulcer-ai-system
```

---

# Backend Setup

```
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Run the backend server:

```
uvicorn app.main:app --reload
```

Backend will start at:

```
http://127.0.0.1:8000
```

API documentation:

```
http://127.0.0.1:8000/docs
```

---

# Frontend Setup

```
cd frontend
npm install
npm run dev
```

Frontend will run at:

```
http://localhost:5173
```

---

# Example Workflow

1. User logs into the system
2. Uploads a foot image and clinical information
3. Backend processes the data using the AI model
4. Prediction and explanation are generated
5. Results are displayed in the dashboard

---

# Explainability

This project emphasizes **model interpretability**.

Two main explanation methods are used:

**Grad-CAM**

Highlights important regions of the image used by the model for prediction.

**SHAP**

Shows how clinical features influence the prediction output.

These techniques help clinicians understand **why the system produced a specific prediction**.

---

# Future Improvements

* Improve model accuracy using larger medical datasets
* Train segmentation models for ulcer area detection
* Add longitudinal patient analysis for healing prediction
* Deploy the system to cloud infrastructure
* Develop a mobile interface for field clinics

---

# Learning Outcomes

This project explores several important concepts in modern AI system development:

* Building production-style APIs using FastAPI
* Integrating deep learning models with web applications
* Designing explainable AI systems
* Using Docker for containerized deployments
* Monitoring AI services using Prometheus and Grafana
* Managing ML experiments using MLflow

---

# System Architecture Diagrams

## Overall System Architecture

<img width="4992" height="916" alt="architecture" src="https://github.com/user-attachments/assets/90d6f38f-e2e9-4a13-9440-54bb0631bfbb" />

---

## Prediction Pipeline (AI Workflow)

<img width="1063" height="1683" alt="pipeline" src="https://github.com/user-attachments/assets/fd0fcbcc-1502-47b2-b63a-5ff43791e72a" />

---

## Ulcer Progression Tracking

<img width="1150" height="1345" alt="progression" src="https://github.com/user-attachments/assets/914ba666-da7d-4772-ae9a-0ee1cd22b298" />

---

## Backend API Flow

<img width="2356" height="1266" alt="api-flow" src="https://github.com/user-attachments/assets/d224691b-b6e5-4296-a2a5-c5fcff5f74e6" />

---

# License

This project is intended for **educational and research purposes only**.
