import os
import shutil
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
from backend.models.interview_code import InterviewCode
from backend.models.submission import Submission
from backend.models.user import User
from backend.config import settings

def validate_interview_code(db: Session, code_str: str) -> InterviewCode:
    code = db.query(InterviewCode).filter(InterviewCode.code == code_str).first()
    if not code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview code not found"
        )
    
    if code.expiry_date and code.expiry_date < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interview code has expired"
        )
    
    return code

def save_video_upload(video_file: UploadFile) -> str:
    # Ensure upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Generate unique filename
    file_extension = os.path.splitext(video_file.filename)[1]
    if not file_extension:
        file_extension = ".mp4" # fallback
    
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    # Save file using streaming to handle large videos
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(video_file.file, buffer)
        
    return file_path

def create_submission(db: Session, user: User, code_str: str, topic_taught: str, video_path: str) -> Submission:
    # Validate code exists
    code = validate_interview_code(db, code_str)
    
    # Check for duplicate submission (UniqueConstraint in DB will also catch this)
    existing = db.query(Submission).filter(
        Submission.user_id == user.id,
        Submission.interview_code_id == code.id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already submitted an interview for this code"
        )
    
    db_submission = Submission(
        user_id=user.id,
        interview_code_id=code.id,
        topic_taught=topic_taught,
        video_url=video_path,
        status="uploaded"
    )
    
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    return db_submission
