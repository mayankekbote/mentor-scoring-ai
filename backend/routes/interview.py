from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.utils.dependencies import get_current_user
from backend.models.user import User
from backend.schemas.interview_schema import (
    CodeValidationRequest, 
    CodeValidationResponse, 
    InterviewSubmissionRequest,
    UploadResponse
)
from backend.services import interview_service, evaluation_service

router = APIRouter()

@router.post("/validate-code", response_model=CodeValidationResponse)
async def validate_code(request: CodeValidationRequest, db: Session = Depends(get_db)):
    """Validate if an interview code is correct and not expired."""
    code = interview_service.validate_interview_code(db, request.code)
    return {
        "organization_name": code.organization_name,
        "status": "valid"
    }

@router.post("/upload-video", response_model=UploadResponse)
async def upload_video(
    video_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Securely upload a video file. Returns the stored relative path."""
    file_path = interview_service.save_video_upload(video_file)
    return {"video_path": file_path}

@router.post("/submit")
async def submit_interview(
    request: InterviewSubmissionRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Finalize submission and trigger AI evaluation in the background.
    Candidates receive confirmation immediately.
    """
    submission = interview_service.create_submission(
        db=db,
        user=current_user,
        code_str=request.interview_code,
        topic_taught=request.topic_taught,
        video_path=request.video_path
    )
    
    # Trigger AI processing in the background
    background_tasks.add_task(evaluation_service.process_submission_evaluation, submission.id)
    
    return {
        "message": "Your interview submission has been received and is being processed.",
        "submission_id": submission.id
    }

from fastapi.responses import FileResponse
import os
from backend.models.submission import Submission
from backend.utils.security import decode_token

@router.get("/status/{submission_id}")
async def get_submission_status(
    submission_id: int,
    db: Session = Depends(get_db)
):
    """Fetch the current processing status and progress of a submission."""
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
        
    return {
        "status": submission.status,
        "progress": submission.processing_progress,
        "message": submission.processing_message
    }

@router.get("/video/{submission_id}")
async def get_interview_video(
    submission_id: int,
    token: str = None,
    db: Session = Depends(get_db)
):
    """Stream the interview video file. Supports token in query for browser video tags."""
    # Handle authentication manually to support query params
    if not token:
        # If no token in query, it might still be in headers if this is a direct API call
        # but for simple browser tags, we expect it in query.
        raise HTTPException(status_code=401, detail="Authentication required")
        
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
        
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Check if the file exists
    if not os.path.exists(submission.video_url):
        raise HTTPException(status_code=404, detail="Video file not found")
        
    return FileResponse(submission.video_url)
