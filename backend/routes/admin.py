from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models.submission import Submission
from backend.models.evaluation_result import AIResult
from backend.models.user import User
from backend.models.interview_code import InterviewCode
from backend.models.admin import Admin
from backend.utils.dependencies import get_current_admin

router = APIRouter()


from backend.schemas.admin_schema import AdminCreateRequest, AdminDetailResponse, InterviewCallRequest
from backend.schemas.interview_code_schema import InterviewCodeCreateRequest, InterviewCodeResponse
from backend.utils.security import hash_password
from backend.utils.email_service import send_interview_invitation_email
import random
import string
from datetime import datetime, timezone


@router.get("/submissions")
async def get_submissions(
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):
    """List all interview submissions for the current organization."""
    submissions = db.query(Submission)\
        .join(InterviewCode)\
        .filter(InterviewCode.organization_name == admin.organization_name)\
        .join(User)\
        .outerjoin(AIResult)\
        .all()
    
    return [
        {
            "id": s.id,
            "user_name": s.user.name,
            "topic_taught": s.topic_taught,
            "interview_code": s.interview_code.code if s.interview_code else "N/A",
            "status": s.status,
            "score": s.ai_result.score if s.ai_result else None,
            "created_at": s.created_at
        }
        for s in submissions
    ]


@router.get("/results/{submission_id}")
async def get_submission_results(
    submission_id: int,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):
    """Get detailed AI evaluation results for a specific submission."""
    submission = db.query(Submission)\
        .join(InterviewCode)\
        .filter(
            Submission.id == submission_id,
            Submission.status.in_(["completed", "called_for_interview"]),
            InterviewCode.organization_name == admin.organization_name
        ).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found, unauthorized, or evaluation still in progress.")
        
    result = db.query(AIResult).filter(AIResult.submission_id == submission_id).first()
    
    return {
        "submission": {
            "id": submission.id,
            "user_name": submission.user.name,
            "topic_taught": submission.topic_taught,
            "interview_code": submission.interview_code.code if submission.interview_code else "N/A",
            "status": submission.status,
            "created_at": submission.created_at,
            "video_url": submission.video_url,
            "subject_domain": submission.user.subject_domain
        },
        "result": result
    }


@router.post("/create-admin")
async def create_admin(
    request: AdminCreateRequest,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Create a new HR admin within the same organization."""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    try:
        # Create user record
        new_user = User(
            name=request.name,
            email=request.email,
            password_hash=hash_password(request.password),
            organization=current_admin.organization_name # Set user-level org too
        )
        db.add(new_user)
        db.flush() # Get user id
        
        # Create admin record
        new_admin = Admin(
            user_id=new_user.id,
            organization_name=current_admin.organization_name
        )
        db.add(new_admin)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create admin: {str(e)}"
        )
    
    return {"message": "Admin created successfully"}


@router.get("/list-admins", response_model=List[AdminDetailResponse])
async def list_admins(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """List all HR admins in the current admin's organization."""
    admins = db.query(Admin)\
        .join(User, Admin.user_id == User.id)\
        .filter(Admin.organization_name == current_admin.organization_name)\
        .all()
    
    return [
        AdminDetailResponse(
            id=a.id,
            name=a.user.name,
            email=a.user.email,
            organization_name=a.organization_name,
            created_at=a.created_at
        )
        for a in admins
    ]


@router.post("/create-interview-code", response_model=InterviewCodeResponse)
async def create_interview_code(
    request: InterviewCodeCreateRequest,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Generate a unique interview code for the organization."""
    if request.max_attempts <= 0:
        raise HTTPException(status_code=400, detail="Max attempts must be a positive integer")
    
    if request.expiry_date.replace(tzinfo=None) <= datetime.now().replace(tzinfo=None):
        raise HTTPException(status_code=400, detail="Expiry date must be in the future")

    # Generate unique code
    max_retries = 10
    generated_code = ""
    
    for _ in range(max_retries):
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        test_code = f"AI-INT-{random_str}"
        
        # Check uniqueness
        exists = db.query(InterviewCode).filter(InterviewCode.code == test_code).first()
        if not exists:
            generated_code = test_code
            break
    
    if not generated_code:
        raise HTTPException(status_code=500, detail="Failed to generate a unique interview code. Please try again.")

    try:
        new_code = InterviewCode(
            code=generated_code,
            organization_name=current_admin.organization_name,
            created_by_admin=current_admin.id,
            max_attempts=request.max_attempts,
            expiry_date=request.expiry_date
        )
        db.add(new_code)
        db.commit()
        db.refresh(new_code)
        return new_code
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/interview-codes", response_model=List[InterviewCodeResponse])
async def list_interview_codes(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """List all interview codes for the current organization."""
    codes = db.query(InterviewCode).filter(
        InterviewCode.organization_name == current_admin.organization_name
    ).order_by(InterviewCode.created_at.desc()).all()
    
    return codes


@router.post("/call-for-interview/{submission_id}")
async def call_for_interview(
    submission_id: int,
    request: InterviewCallRequest,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Update status and send interview invitation email."""
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    # Verify if submission belongs to same organization
    if submission.interview_code.organization_name != current_admin.organization_name:
        raise HTTPException(status_code=403, detail="Unauthorized access to this submission")

    # Update status
    submission.status = "called_for_interview"
    
    try:
        db.commit()
        db.refresh(submission)
        
        # Prepare email data
        candidate_name = submission.user.name
        candidate_email = submission.user.email
        topic = submission.topic_taught
        ai_score = submission.ai_result.score if submission.ai_result else 0
        organization_name = current_admin.organization_name
        
        # Send email
        send_interview_invitation_email(
            email_to=candidate_email,
            candidate_name=candidate_name,
            topic=topic,
            interview_date=request.interview_date,
            interview_time=request.interview_time,
            organization_name=organization_name,
            ai_score=ai_score
        )
        
        return {"message": "Interview call sent successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
