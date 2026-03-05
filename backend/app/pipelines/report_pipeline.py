"""Clinical report generation pipeline."""

from datetime import datetime
from typing import Dict, Any, Optional
import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ReportData(BaseModel):
    """Data model for report generation."""
    patient_id: str
    prediction_id: str
    predicted_class: str
    confidence: float
    segmentation_area: Optional[float] = None
    clinical_data: Optional[Dict[str, Any]] = None
    explainability_data: Optional[Dict[str, Any]] = None


class ReportPipeline:
    """
    Pipeline for generating clinical reports.
    
    Features:
    - Score interpretation
    - Clinical recommendations
    - Risk assessment
    - Report formatting
    """
    
    SEVERITY_LEVELS = {
        "normal": {"name": "No Ulcer", "severity": 0, "risk": "Low"},
        "ulcer": {"name": "Ulcer", "severity": 1, "risk": "Moderate"},
        "severe": {"name": "Severe Ulcer", "severity": 2, "risk": "High"}
    }
    
    RECOMMENDATIONS = {
        "normal": [
            "Continue regular foot care routine",
            "Monitor for any skin changes",
            "Maintain good hygiene practices"
        ],
        "ulcer": [
            "Schedule follow-up appointment",
            "Increase monitoring frequency",
            "Consider topical treatment"
        ],
        "severe": [
            "Urgent medical attention required",
            "Consider inpatient treatment",
            "Possible antibiotic therapy"
        ]
    }
    
    def __init__(self):
        """Initialize report pipeline."""
        logger.info("Initialized report pipeline")
    
    def generate_report(self, data: ReportData) -> Dict[str, Any]:
        """
        Generate comprehensive clinical report.
        
        Args:
            data: Report data
        
        Returns:
            Generated report dictionary
        """
        try:
            # Interpret prediction
            interpretation = self.SEVERITY_LEVELS.get(
                data.predicted_class,
                self.SEVERITY_LEVELS["normal"]
            )
            
            # Get recommendations
            recommendations = self.RECOMMENDATIONS.get(
                data.predicted_class,
                []
            )
            
            # Build report
            report = {
                "report_id": f"RPT-{datetime.now().timestamp()}",
                "generated_at": datetime.now().isoformat(),
                "patient_id": data.patient_id,
                "prediction_id": data.prediction_id,
                "prediction": {
                    "class": data.predicted_class,
                    "confidence": round(float(data.confidence), 4),
                    "interpretation": interpretation["name"],
                    "severity_level": interpretation["severity"],
                    "risk_assessment": interpretation["risk"]
                },
                "clinical_findings": self._extract_clinical_findings(data),
                "recommendations": recommendations,
                "next_steps": self._get_next_steps(data.predicted_class),
                "metadata": {
                    "model_version": "1.0",
                    "algorithm": "CNN + Multimodal Fusion",
                    "confidence_threshold": 0.7
                }
            }
            
            logger.info(f"Generated report {report['report_id']} for patient {data.patient_id}")
            return report
        
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            raise
    
    def _extract_clinical_findings(self, data: ReportData) -> Dict[str, Any]:
        """Extract clinical findings from prediction."""
        findings = {
            "ulcer_detected": data.predicted_class != "normal",
            "confidence": round(float(data.confidence), 4)
        }
        
        if data.segmentation_area is not None:
            findings["affected_area_percentage"] = round(
                float(data.segmentation_area) * 100, 2
            )
        
        if data.clinical_data:
            findings["clinical_factors"] = data.clinical_data
        
        return findings
    
    def _get_next_steps(self, prediction_class: str) -> list:
        """Get recommended next steps based on prediction."""
        next_steps_map = {
            "normal": [
                "Schedule routine follow-up in 3-6 months",
                "Perform regular home assessments"
            ],
            "ulcer": [
                "Schedule medical appointment within 1-2 weeks",
                "Increase observation frequency",
                "Document wound characteristics"
            ],
            "severe": [
                "Seek immediate medical attention",
                "Schedule urgent hospital visit",
                "Prepare detailed documentation for specialist"
            ]
        }
        
        return next_steps_map.get(prediction_class, [])
    
    def export_report(self, report: Dict[str, Any], format: str = "json") -> str:
        """
        Export report in specified format.
        
        Args:
            report: Report dictionary
            format: Export format (json, csv, pdf)
        
        Returns:
            Exported report as string
        """
        if format == "json":
            import json
            return json.dumps(report, indent=2)
        elif format == "csv":
            return self._export_csv(report)
        elif format == "pdf":
            logger.warning("PDF export not yet implemented")
            return "PDF export not available"
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _export_csv(self, report: Dict[str, Any]) -> str:
        """Export report as CSV."""
        lines = [
            f"Report ID,{report.get('report_id', '')}",
            f"Patient ID,{report.get('patient_id', '')}",
            f"Generated At,{report.get('generated_at', '')}",
            f"Prediction,{report.get('prediction', {}).get('class', '')}",
            f"Confidence,{report.get('prediction', {}).get('confidence', '')}",
            f"Interpretation,{report.get('prediction', {}).get('interpretation', '')}",
            f"Risk Level,{report.get('prediction', {}).get('risk_assessment', '')}"
        ]
        return "\n".join(lines)


def create_report_pipeline() -> ReportPipeline:
    """Create and return report pipeline."""
    return ReportPipeline()
