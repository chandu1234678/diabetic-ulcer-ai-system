"""Image upload routes for handling ulcer image uploads."""

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import logging

router = APIRouter(prefix="/images", tags=["images"])
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "tiff"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload an ulcer image for analysis.
    
    Args:
        file: Image file (JPEG, PNG, or TIFF)
    
    Returns:
        Image metadata and processing status
    """
    try:
        # Validate file extension
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Validate file size
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE / 1024 / 1024}MB"
            )
        
        logger.info(f"Image uploaded: {file.filename}")
        
        return {
            "filename": file.filename,
            "size": len(contents),
            "content_type": file.content_type,
            "status": "success"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading image: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to upload image")


@router.get("/list")
async def list_images():
    """List all uploaded images."""
    try:
        # TODO: Implement database query to get list of images
        return {"images": [], "count": 0}
    except Exception as e:
        logger.error(f"Error listing images: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list images")
