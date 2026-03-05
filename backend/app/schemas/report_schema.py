"""Report-related schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class PredictionData(BaseModel):
    """Prediction data in report."""
    predicted_class: str
    confidence: float = Field(ge=0, le=1)
    interpretation: str
    severity_level: int = Field(ge=0, le=2)
    risk_assessment: str


class ClinicalFindings(BaseModel):
    """Clinical findings in report."""
    ulcer_detected: bool
    confidence: float
    affected_area_percentage: Optional[float] = Field(None, ge=0, le=100)
    clinical_factors: Optional[Dict[str, Any]] = None


class ReportGenerationRequest(BaseModel):
    """Request to generate report."""
    patient_id: str
    prediction_id: str
    include_explainability: bool = True
    include_clinical_data: bool = True
    include_recommendations: bool = True


class ReportData(BaseModel):
    """Complete report data."""
    report_id: str
    generated_at: datetime
    patient_id: str
    prediction_id: str
    prediction: PredictionData
    clinical_findings: ClinicalFindings
    recommendations: List[str]
    next_steps: List[str]
    metadata: Dict[str, Any]


class ReportExportRequest(BaseModel):
    """Request to export report."""
    report_id: str
    format: str = Field(..., regex="^(pdf|json|csv)$")
    include_attachments: bool = False


class ReportExportResponse(BaseModel):
    """Response for report export."""
    report_id: str
    format: str
    file_url: str
    generated_at: datetime
    file_size: int


class ReportListResponse(BaseModel):
    """Response for listing reports."""
    total_count: int = Field(ge=0)
    reports: List[Dict[str, Any]]
    pagination: Optional[Dict[str, Any]] = None


class ReportSummary(BaseModel):
    """Summary of a report."""
    report_id: str
    patient_id: str
    prediction_id: str
    generated_at: datetime
    risk_level: str
    ulcer_detected: bool


class ComparisonReport(BaseModel):
    """Report comparing multiple predictions."""
    comparison_id: str
    patient_id: str
    prediction_ids: List[str]
    timeline: List[datetime]
    progression: str  # "Improving", "Stable", "Worsening"
    trend_analysis: Dict[str, Any]
    clinical_significance: str
    recommendations: List[str]
