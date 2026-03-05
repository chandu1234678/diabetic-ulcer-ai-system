# System Architecture

## Overview

The Diabetic Ulcer AI System is a comprehensive web-based diagnostic platform that uses advanced machine learning algorithms to detect and analyze diabetic ulcers from medical images combined with clinical data.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     Client Layer (Frontend)                      │
│                                                                   │
│  React SPA - Dashboard, Prediction, Reports, Clinical Data      │
│                                                                   │
└────────────────────────┬──────────────────────────────────────────┘
                         │
                         │ HTTP/REST API
                         │
┌────────────────────────▼──────────────────────────────────────────┐
│                   API Gateway (Nginx)                              │
│                                                                    │
│  - Request routing                                                │
│  - Load balancing                                                 │
│  - Authentication                                                 │
│  - Rate limiting                                                  │
└────────────────────────┬───────────────────────────────────────────┘
                         │
              ┌──────────┴────────────┐
              │                       │
┌─────────────▼──────────┐  ┌────────▼──────────────┐
│  FastAPI Backend       │  │  WebSocket Server     │
│                        │  │  (Real-time updates)  │
│  - Image Upload        │  │                       │
│  - Prediction API      │  │                       │
│  - Clinical Data API   │  │                       │
│  - Report Generation   │  │                       │
│  - Authentication      │  │                       │
└─────────────┬──────────┘  └──────────────────────┘
              │
    ┌─────────┴───────────┬──────────────┬──────────────┐
    │                     │              │              │
┌───▼────────┐  ┌────────▼────┐  ┌─────▼─────┐  ┌────▼────────┐
│  ML Service │  │ Image Svc   │  │ Clinical  │  │ Report Svc  │
│             │  │             │  │ Data Svc  │  │             │
│ - CNN Model │  │ - Upload    │  │ - Scoring │  │ - Generation│
│ - Segmenting│  │ - Processing│  │ - Risk    │  │ - Export    │
│ - Multimodal│  │ - Quality   │  │ - Storage │  │ - Template  │
└───┬────────┘  └────┬────────┘  └─────┬─────┘  └────┬────────┘
    │                │                  │            │
    └────────────────┼──────────────────┼────────────┘
                     │
        ┌────────────┴─────────────┐
        │                          │
┌───────▼─────────┐    ┌──────────▼────────┐
│   PostgreSQL    │    │  Model Weights    │
│   Database      │    │  Storage (S3/NFS) │
│                 │    │                   │
│ - Patients      │    │ - CNN weights     │
│ - Images        │    │ - Segmentation    │
│ - Predictions   │    │ - Multimodal      │
│ - Reports       │    │ - Exp. Models     │
└─────────────────┘    └───────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                  Monitoring & Logging                            │
│                                                                   │
│  Prometheus metrics → Grafana dashboards → ELK logs              │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Frontend (React)
- **Purpose**: User interface for clinicians and administrators
- **Technology**: React 18, Redux for state management
- **Features**:
  - Patient management dashboard
  - Image upload and analysis interface
  - Real-time prediction results
  - Clinical report generation and export
  - Explainability visualization (Heatmaps, SHAP)

### 2. Backend (FastAPI)
- **Purpose**: RESTful API server handling all business logic
- **Technology**: FastAPI, Python 3.9+
- **Routes**:
  - `/health` - Health check
  - `/predict` - Get predictions
  - `/clinical-data` - Manage patient clinical data
  - `/images` - Image management
  - `/reports` - Report generation and management
  - `/explain` - Get explainability data

### 3. ML Service
- **Purpose**: Model inference and predictions
- **Models**:
  - **CNN**: 3-class classification (Normal/Ulcer/Severe)
  - **Segmentation**: U-Net for ulcer boundary detection
  - **Multimodal**: Fusion of image + clinical data
- **Framework**: PyTorch

### 4. Database (PostgreSQL)
- **Purpose**: Store application data
- **Tables**:
  - Users and authentication
  - Patients and clinical data
  - Images and predictions
  - Reports and audit logs

### 5. Storage (S3/NFS)
- **Purpose**: Store model weights and large files
- **Contents**:
  - Pre-trained model weights
  - Uploaded images (temporary)
  - Generated reports

## Data Flow

### Prediction Flow
1. User uploads ulcer image via frontend
2. FastAPI receives image, validates format/size
3. Image preprocessing (normalization, resizing)
4. CNN model inference
5. Segmentation model inference (optional)
6. Confidence thresholding and risk classification
7. Return results to frontend

### Explainability Flow
1. Request explainability for a prediction
2. Load saved prediction data
3. Generate explanations:
   - Grad-CAM heatmaps
   - SHAP values
   - Feature importance
4. Format and return visualizations

### Report Generation Flow
1. Collect prediction + clinical data
2. Risk assessment calculation
3. Generate recommendations
4. Format into PDF/JSON/CSV
5. Store in database
6. Return to user

## Deployment Architecture

### Docker Compose (Development)
- Single container for backend
- Single container for frontend
- PostgreSQL service
- Nginx reverse proxy

### Kubernetes (Production)
- Multiple backend replicas (auto-scaling)
- Multiple frontend replicas
- Persistent volumes for model weights
- StatefulSet for database
- Service mesh (optional)
- Ingress controller for routing

## Security Considerations

1. **Authentication**: JWT tokens, API key validation
2. **Authorization**: Role-based access control (RBAC)
3. **Data Protection**: Encrypted storage, TLS/SSL
4. **Input Validation**: File type, size, and content checks
5. **Rate Limiting**: API rate limits to prevent abuse
6. **Audit Logging**: All predictions logged for compliance

## Scalability Strategy

1. **Horizontal Scaling**: Multiple backend instances
2. **Caching**: Redis for frequently accessed data
3. **Asynchronous Processing**: Celery for long-running tasks
4. **Load Balancing**: Nginx round-robin or HAProxy
5. **Database Optimization**: Indexing critical columns
6. **Model Optimization**: Model quantization and TensorRT

## Performance Targets

- Prediction latency: < 2 seconds
- API response time: < 500ms
- System uptime: 99.5%
- Throughput: 100+ predictions/minute
- Model accuracy: > 94%

## Monitoring and Observability

- **Prometheus**: Metrics collection
- **Grafana**: Visualization dashboards
- **ELK Stack**: Centralized logging
- **Jaeger**: Distributed tracing (optional)
- **Custom Metrics**: Model performance, business metrics
