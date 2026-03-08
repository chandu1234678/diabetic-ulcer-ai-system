# Health Metrics Assessment API Documentation

## Overview
The Health Metrics Assessment API provides a comprehensive system for:
- Calculating personalized health risk scores
- Generating medical recommendations
- Tracking patient health metrics
- Assessing diabetic foot ulcer risk

## Base URL
```
/health-metrics
```

---

## Endpoints

### 1. Assess Health Metrics
**POST** `/health-metrics/assess`

Calculates a comprehensive health assessment based on patient metrics.

#### Request Body
```json
{
  "age": 45,
  "bmi": 28.5,
  "blood_sugar": 150,
  "diabetes_duration": 8
}
```

#### Request Parameters
| Parameter | Type | Required | Range | Description |
|-----------|------|----------|-------|-------------|
| age | integer | Yes | 1-150 | Patient age in years |
| bmi | float | Yes | 10-60 | Body Mass Index |
| blood_sugar | integer | Yes | 40-500 | Blood sugar level in mg/dL |
| diabetes_duration | integer | No | 0+ | Years with diabetes |

#### Response (200 OK)
```json
{
  "risk_score": 52.5,
  "risk_level": "Moderate Risk",
  "recommendations": [
    "Implement a gradual weight loss plan (0.5-1 kg per week) through diet and exercise",
    "Monitor blood glucose regularly (3+ times daily) and adjust medications if needed",
    "Schedule preventive health screenings annually",
    "Maintain a consistent exercise routine (150 mins/week)",
    "Regular foot examinations for early detection of potential ulcers"
  ],
  "details": {
    "bmi_category": "Overweight",
    "sugar_level": "High",
    "age_group": "Adult",
    "bmi_value": "28.5",
    "blood_sugar_value": "150 mg/dL"
  },
  "explanation": "Your assessment shows Moderate Risk. You are in the Adult category with a Overweight BMI and High blood sugar level. While not critical, there are areas for improvement. Focus on the recommended lifestyle changes to reduce your risk."
}
```

---

### 2. Calculate Ulcer Risk
**POST** `/health-metrics/calculate-ulcer-risk`

Calculates specific diabetic foot ulcer risk based on health metrics and history.

#### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| age | integer | Yes | Patient age |
| bmi | float | Yes | Body Mass Index |
| blood_sugar | integer | Yes | Blood sugar level |
| diabetes_duration | integer | No | Years with diabetes |
| has_infection | boolean | No | Has active infection (adds 20% risk) |
| previous_ulcers | boolean | No | History of ulcers (adds 25% risk) |

#### Example Request
```
/health-metrics/calculate-ulcer-risk?age=50&bmi=32&blood_sugar=200&diabetes_duration=10&has_infection=false&previous_ulcers=true
```

#### Response (200 OK)
```json
{
  "ulcer_risk_score": 65.3,
  "recommendation": "Regular foot monitoring recommended",
  "factors": {
    "age_factor": "Middle-aged",
    "bmi_factor": "Obese",
    "blood_sugar_factor": "Critical",
    "infection_present": false,
    "ulcer_history": true
  }
}
```

---

### 3. Generate Health Report
**POST** `/health-metrics/generate-report`

Generates a comprehensive health assessment report.

#### Request Body
```json
{
  "age": 55,
  "bmi": 26.5,
  "blood_sugar": 120,
  "diabetes_duration": 12
}
```

#### Response (200 OK)
```json
{
  "report_type": "Health Assessment Report",
  "risk_score": 45.2,
  "risk_level": "Moderate Risk",
  "metrics": {
    "age": 55,
    "bmi": 26.5,
    "blood_sugar": 120,
    "diabetes_duration": 12
  },
  "recommendations": [
    "Continue regular blood glucose monitoring",
    "Intensive foot care and regular podiatry examinations are essential",
    "Maintain HbA1c levels below 7% for better diabetes control",
    "Maintain a consistent exercise routine (150 mins/week)",
    "Regular foot examinations for early detection of potential ulcers"
  ],
  "generated_at": "2024-03-06",
  "next_review_date": "2024-04-06"
}
```

---

## Risk Score Calculation

### Formula
```
Risk Score = (Age Risk × 0.20) + (BMI Risk × 0.25) + (Blood Sugar Risk × 0.40) + (Diabetes Risk × 0.15)
```

### BMI Categories and Risk Weights
| Category | Range | Risk Weight |
|----------|-------|-------------|
| Underweight | < 18.5 | 15.0 |
| Normal | 18.5 - 24.9 | 5.0 |
| Overweight | 25.0 - 29.9 | 25.0 |
| Obese | ≥ 30.0 | 40.0 |

### Blood Sugar Categories and Risk Weights
| Category | Range (mg/dL) | Risk Weight |
|----------|--|-------------|
| Low | < 100 | 20.0 |
| Normal | 100 - 125 | 5.0 |
| High | 126 - 199 | 35.0 |
| Critical | ≥ 200 | 50.0 |

### Age Risk Groups and Weights
| Age Group | Range | Risk Weight |
|-----------|-------|-------------|
| Young Adult | < 30 | 10.0 |
| Adult | 30 - 44 | 20.0 |
| Middle-aged | 45 - 59 | 30.0 |
| Senior | ≥ 60 | 40.0 |

### Overall Risk Levels
| Risk Level | Score Range |
|-----------|----------|
| Low Risk | 0 - 30 |
| Moderate Risk | 30 - 60 |
| High Risk | 60 - 100 |

---

## Error Handling

### Example Error Response
```json
{
  "detail": "Invalid input - Age must be between 1 and 150"
}
```

### Common HTTP Status Codes
| Status | Meaning |
|--------|---------|
| 200 | Successful assessment |
| 400 | Invalid input parameters |
| 422 | Validation error |
| 500 | Server error |

---

## Frontend Integration

### JavaScript Example
```javascript
import { getHealthMetricsAssessment } from '../services/api'

// Call the API
const assessment = await getHealthMetricsAssessment({
  age: 45,
  bmi: 28.5,
  blood_sugar: 150,
})

// Use the response
console.log(`Risk Score: ${assessment.risk_score}`)
console.log(`Risk Level: ${assessment.risk_level}`)
console.log(`Recommendations:`, assessment.recommendations)
```

---

## React Component Usage

### HealthMetricsForm Component
```jsx
import HealthMetricsForm from './components/HealthMetricsForm'

export default function MyComponent() {
  const [age, setAge] = useState('')
  const [bmi, setBmi] = useState('')
  const [sugar, setSugar] = useState('')

  return (
    <HealthMetricsForm
      age={age}
      setAge={setAge}
      bmi={bmi}
      setBmi={setBmi}
      sugarBeforeFast={sugar}
      setSugarBeforeFast={setSugar}
      compact={true}
    />
  )
}
```

### Features
- Real-time validation
- Interactive risk assessment display
- Color-coded risk indicators
- Personalized recommendations
- Automatic API calls on input change

---

## Database Models

### HealthMetrics Table
```sql
CREATE TABLE health_metrics (
  id INT PRIMARY KEY,
  user_id INT FOREIGN KEY,
  age INT,
  bmi FLOAT,
  blood_sugar FLOAT,
  diabetes_duration INT,
  risk_score FLOAT,
  risk_level VARCHAR(50),
  recommendations TEXT,
  created_at DATETIME
);
```

---

## Installation & Setup

### Backend
1. Health metrics router is auto-registered in `main.py`
2. Database models are in `models.py`
3. No additional dependencies required (uses existing FastAPI/Pydantic)

### Frontend
1. HealthMetricsForm component is in `frontend/src/components/`
2. API function is in `frontend/src/services/api.js`
3. Already integrated in Signup and FootScanAnalysis pages

---

## Testing

### Test Cases
```bash
# Test assessment endpoint
curl -X POST http://localhost:8000/health-metrics/assess \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "bmi": 28.5,
    "blood_sugar": 150,
    "diabetes_duration": 8
  }'

# Test ulcer risk calculation
curl -X POST http://localhost:8000/health-metrics/calculate-ulcer-risk \
  -H "Content-Type: application/json" \
  -d '{
    "age": 50,
    "bmi": 32,
    "blood_sugar": 200,
    "has_infection": false,
    "previous_ulcers": true
  }'
```

---

## Performance Notes
- Risk calculations are instant (< 10ms)
- No database queries required for assessments
- Assessments are cached at frontend level
- Metrics are stored in database for historical tracking

---

## Future Enhancements
- [ ] Predictive modeling with historical data
- [ ] ML-based risk adjustment factors
- [ ] Integration with wearable devices
- [ ] Real-time monitoring alerts
- [ ] Trend analysis and progression tracking
- [ ] Export reports as PDF
