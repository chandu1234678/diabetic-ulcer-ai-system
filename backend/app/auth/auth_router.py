from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models import User
from backend.app.schemas import UserCreate, UserLogin, TokenResponse, UserForgotPassword, UserResetPassword
from backend.app.auth.password_utils import hash_password, verify_password
from backend.app.auth.jwt_handler import create_access_token
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.password_reset_handler import (
    generate_password_reset_token,
    verify_password_reset_token,
    send_password_reset_email
)
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user:
        # Log for debugging
        import sys
        print(f"User not found: {user.email}", file=sys.stderr)
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password with detailed logging
    password_valid = verify_password(user.password, db_user.hashed_password)
    
    if not password_valid:
        # Log for debugging
        import sys
        print(f"Password mismatch for user: {user.email}", file=sys.stderr)
        print(f"Stored hash: {db_user.hashed_password[:50]}...", file=sys.stderr)
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=dict)
def get_current_user_info(user: User = Depends(get_current_user)):
    """Get current authenticated user info."""
    return {
        "id": user.id,
        "email": user.email,
        "is_active": user.is_active,
        "created_at": user.created_at
    }

@router.post("/forgot-password")
def forgot_password(request: UserForgotPassword, db: Session = Depends(get_db)):
    """
    Request a password reset token to be sent to the user's email.
    """
    user = db.query(User).filter(User.email == request.email).first()
    
    # Always return same message for security
    base_message = "If an account exists with this email, a password reset link will be sent."
    
    if not user:
        # For development: still return the base message but skip token generation
        from backend.app.config import settings
        if settings.environment == "development" and not settings.smtp_username:
            return {
                "message": base_message,
                "reset_link": None,
                "note": "User email not found in database"
            }
        return {"message": base_message}
    
    # Generate reset token
    reset_token = generate_password_reset_token(user.email)
    
    # Send email (in dev mode, logs the link)
    success = send_password_reset_email(user.email, reset_token)
    
    if not success:
        raise HTTPException(
            status_code=500,
            detail="Failed to send password reset email. Please try again later."
        )
    
    from app.config import settings
    reset_link = f"{settings.frontend_url}/reset-password?token={reset_token}"
    
    # In development without SMTP, return the link
    if settings.environment == "development" and not settings.smtp_username:
        return {
            "message": base_message,
            "reset_link": reset_link,
            "note": "[DEV MODE] Reset link generated (no email sent). Copy the link above to reset password."
        }
    
    return {"message": "Password reset email sent successfully"}


@router.post("/reset-password", response_model=TokenResponse)
def reset_password(request: UserResetPassword, db: Session = Depends(get_db)):
    """
    Reset user password using a valid reset token.
    """
    # Verify the reset token
    email = verify_password_reset_token(request.token)
    
    if not email:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired password reset token"
        )
    
    # Find user by email
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    # Update password
    user.hashed_password = hash_password(request.new_password)
    db.commit()
    
    # Generate new access token
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
