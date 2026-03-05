# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication
All API endpoints (except `/health`) require JWT authentication.

```
Authorization: Bearer <jwt_token>
```

## Endpoints

### Health Check
```
GET /health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Prediction Endpoints

#### Submit Prediction
```
POST /predict
Content-Type: multipart/form-data

Parameters:
- image: File (required) - Image file (JPEG, PNG, TIFF)
- clinical_data: JSON (optional) - Clinical data object
```

Response:
```json
{
  "prediction_id": "pred-123456",
  "predicted_class": "ulcer",
  "confidence": 0.92,
  "severity": "Moderate",
  "risk_level": "High",
  "affected_area_percentage": 8.5,
  "processing_time_ms": 1200,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### Get Prediction
```
GET /predict/{prediction_id}
```

Response: Same as above

#### List Predictions
```
GET /predict?patient_id={patient_id}&limit=10&offset=0
```

### Image Endpoints

#### Upload Image
```
POST /images/upload
Content-Type: multipart/form-data

Parameters:
- file: File (required) - Image file
```

Response:
```json
{
  "image_id": "img-123456",
  "filename": "ulcer_sample.jpg",
  "size": 256000,
  "content_type": "image/jpeg",
  "status": "success"
}
```

#### List Images
```
GET /images/list
```

### Clinical Data Endpoints

#### Submit Clinical Data
```
POST /clinical-data
Content-Type: application/json

Body:
{
  "patient_id": "P123456",
  "age": 55,
  "gender": "M",
  "diabetes_type": "Type 2",
  "duration_of_diabetes": 10.5,
  "hba1c_level": 7.8,
  "bmi": 28.5,
  "smoking_status": "Former",
  "neuropathy": true,
  "infection_status": false,
  "previous_ulcers": 1
}
```

Response:
```json
{
  "patient_id": "P123456",
  "stored_at": "2024-01-15T10:30:00Z"
}
```

#### Get Clinical Data
```
GET /clinical-data/{patient_id}
```

#### Risk Assessment
```
GET /clinical-data/{patient_id}/risk-assessment
```

Response:
```json
{
  "patient_id": "P123456",
  "total_score": 45,
  "risk_level": "High",
  "risk_factors": ["Peripheral neuropathy", "Poor glycemic control"],
  "recommendations": [
    "Intensive wound care protocol",
    "Monthly professional assessments"
  ],
  "monitoring_frequency": "Monthly"
}
```

### Report Endpoints

#### Generate Report
```
POST /reports/generate
Content-Type: application/json

Body:
{
  "patient_id": "P123456",
  "prediction_id": "pred-123456",
  "include_explainability": true,
  "include_clinical_data": true
}
```

Response:
```json
{
  "report_id": "rpt-123456",
  "patient_id": "P123456",
  "prediction_id": "pred-123456",
  "generated_at": "2024-01-15T10:30:00Z",
  "status": "generated"
}
```

#### Get Report
```
GET /reports/{report_id}
```

#### List Reports
```
GET /reports/list/{patient_id}?limit=10&offset=0
```

#### Export Report
```
POST /reports/{report_id}/export
Content-Type: application/json

Body:
{
  "format": "pdf"  // pdf, json, csv
}
```

Response:
```json
{
  "report_id": "rpt-123456",
  "format": "pdf",
  "file_url": "http://localhost:8000/reports/rpt-123456/file.pdf",
  "generated_at": "2024-01-15T10:30:00Z"
}
```

### Explainability Endpoints

#### Get Explanation
```
GET /explain/{prediction_id}?method=gradcam
Query Parameters:
- method: String - "gradcam", "shap", "lime" (default: "gradcam")
```

Response:
```json
{
  "prediction_id": "pred-123456",
  "method": "gradcam",
  "heatmap_url": "http://localhost:8000/static/heatmaps/pred-123456.png",
  "feature_importance": {...},
  "interpretation": "High activation in left foot region"
}
```

## Error Handling

### Error Response Format
```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "details": {...}
}
```

### Common Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 413 | Payload Too Large |
| 500 | Internal Server Error |

### Example Error

```json
{
  "error": "INVALID_IMAGE_FORMAT",
  "message": "Unsupported image format. Allowed: JPEG, PNG, TIFF",
  "details": {
    "provided": "BMP",
    "allowed": ["JPEG", "PNG", "TIFF"]
  }
}
```

## Rate Limiting

API endpoints are rate-limited to 100 requests per minute per client.

Response headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1705329000
```

## Examples

### Complete Prediction Workflow

1. **Upload Image**
```bash
curl -X POST http://localhost:8000/api/images/upload \
  -H "Authorization: Bearer token" \
  -F "file=@ulcer.jpg"
```

2. **Submit Clinical Data**
```bash
curl -X POST http://localhost:8000/api/clinical-data \
  -H "Authorization: Bearer token" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "P123456",
    "age": 55,
    "diabetes_type": "Type 2",
    ...
  }'
```

3. **Run Prediction**
```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Authorization: Bearer token" \
  -F "image=@ulcer.jpg" \
  -F "clinical_data={...}"
```

4. **Generate Report**
```bash
curl -X POST http://localhost:8000/api/reports/generate \
  -H "Authorization: Bearer token" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "P123456",
    "prediction_id": "pred-123456"
  }'
```

## OpenAPI/Swagger

Interactive API documentation available at:
```
http://localhost:8000/docs
```

Redoc documentation:
```
http://localhost:8000/redoc
```
