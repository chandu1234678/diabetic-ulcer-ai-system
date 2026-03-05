"""Image-related schemas."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ImageMetadata(BaseModel):
    """Image metadata schema."""
    filename: str
    size: int = Field(..., gt=0)
    content_type: str
    width: int = Field(..., gt=0)
    height: int = Field(..., gt=0)
    format: str
    uploaded_at: datetime


class ImageUploadResponse(BaseModel):
    """Response for image upload."""
    image_id: str
    filename: str
    size: int
    content_type: str
    status: str
    message: Optional[str] = None
    uploaded_at: datetime


class ImageQualityReport(BaseModel):
    """Image quality assessment report."""
    image_id: str
    brightness: float = Field(ge=0, le=255)
    contrast: float = Field(ge=0)
    sharpness: float = Field(ge=0)
    quality_score: float = Field(ge=0, le=1)
    dimensions: tuple
    assessment_passed: bool
    recommendations: list


class ImageProcessingRequest(BaseModel):
    """Request for image processing."""
    image_id: str
    apply_enhancement: bool = False
    apply_segmentation: bool = True
    target_size: Optional[tuple] = Field(None, example=(224, 224))


class SegmentationResult(BaseModel):
    """Segmentation result schema."""
    image_id: str
    mask_id: str
    affected_area_percentage: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=1)
    bounding_box: Optional[dict] = None
    processing_time_ms: int


class ImageListResponse(BaseModel):
    """Response for listing images."""
    total_count: int = Field(ge=0)
    images: list
    pagination: Optional[dict] = None
