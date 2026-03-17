from fastapi import APIRouter, Depends, Body, File, UploadFile, Form
import os
import shutil
import uuid
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.user_schema import UserCreate, UserLogin, UserResponse
from backend.schemas.auth_schema import PasswordResetRequest, PasswordResetConfirm
from backend.services import auth_service

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    age: int = Form(None),
    subject_domain: str = Form(None),
    years_experience: int = Form(None),
    organization: str = Form(None),
    resume: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    """Register a new user (candidate by default) with an optional resume."""
    resume_url = None
    if resume:
        # Create storage directory if it doesn't exist
        upload_dir = "backend/storage/resumes"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file with unique name
        file_ext = os.path.splitext(resume.filename)[1]
        file_name = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(upload_dir, file_name)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)
        
        resume_url = f"storage/resumes/{file_name}"

    user_in = UserCreate(
        name=name,
        email=email,
        password=password,
        age=age,
        subject_domain=subject_domain,
        years_experience=years_experience,
        organization=organization,
        resume_url=resume_url
    )
    return auth_service.register_user(db, user_in)

@router.post("/login")
async def login(login_in: UserLogin, db: Session = Depends(get_db)):
    """Login and receive a JWT access token & user info (including is_admin)."""
    return auth_service.authenticate_user(db, login_in)

@router.post("/request-password-reset")
async def request_password_reset(request_in: PasswordResetRequest, db: Session = Depends(get_db)):
    """Request a password reset token via email."""
    auth_service.request_password_reset(db, request_in.email)
    return {"message": "If the email exists, a reset token has been generated."}

@router.post("/reset-password")
async def reset_password(reset_in: PasswordResetConfirm, db: Session = Depends(get_db)):
    """Reset password using a valid token."""
    auth_service.reset_password(db, reset_in.token, reset_in.new_password)
    return {"message": "Password updated successfully."}
