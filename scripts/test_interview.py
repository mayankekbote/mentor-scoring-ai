import sys
from pathlib import Path
import os
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import io
from fastapi import UploadFile

# Add project root to sys.path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from backend.database import SessionLocal, engine, Base
from backend.services import interview_service, auth_service
from backend.schemas.user_schema import UserCreate
from backend.models import User, Admin, InterviewCode, Submission, AIResult

def cleanup(db: Session, email: str, code_str: str):
    """Cleanup test data."""
    # Delete codes first as they reference admins
    db.query(InterviewCode).filter(InterviewCode.code == code_str).delete()
    
    user = db.query(User).filter(User.email == email).first()
    if user:
        submissions = db.query(Submission).filter(Submission.user_id == user.id).all()
        for s in submissions:
            db.query(AIResult).filter(AIResult.submission_id == s.id).delete()
            db.query(Submission).filter(Submission.id == s.id).delete()
        db.query(Admin).filter(Admin.user_id == user.id).delete()
        db.query(User).filter(User.id == user.id).delete()
        
    db.commit()

def test_interview_flow():
    db = SessionLocal()
    user_email = "candidate_test@example.com"
    code_str = "TEST-CODE-2024"
    
    try:
        print("--- Initializing Test Data ---")
        cleanup(db, user_email, code_str)
        
        # 1. Create User
        user_in = UserCreate(
            name="Interview Candidate",
            email=user_email,
            password="password123",
            organization="Test Org"
        )
        user = auth_service.register_user(db, user_in)
        
        # 2. Create Admin (to own the code)
        admin_entry = Admin(user_id=user.id, organization_name="Test Org")
        db.add(admin_entry)
        db.commit()
        db.refresh(admin_entry)
        
        # 3. Create Interview Code
        code_entry = InterviewCode(
            code=code_str,
            organization_name="Test Org",
            created_by_admin=admin_entry.id,
            expiry_date=datetime.now(timezone.utc) + timedelta(days=7)
        )
        db.add(code_entry)
        db.commit()
        
        print("\n--- Testing Code Validation ---")
        validated_code = interview_service.validate_interview_code(db, code_str)
        print(f"Code '{code_str}' validated for organization: {validated_code.organization_name}")
        
        print("\n--- Testing Video Upload (Mock) ---")
        # Since we're in a script, we mock the UploadFile
        mock_video_content = b"fake video content"
        mock_file = io.BytesIO(mock_video_content)
        upload_file = UploadFile(filename="test_interview.mp4", file=mock_file)
        
        video_path = interview_service.save_video_upload(upload_file)
        print(f"Video saved to: {video_path}")
        
        print("\n--- Testing Submission ---")
        submission = interview_service.create_submission(
            db=db,
            user=user,
            code_str=code_str,
            topic_taught="Mathematics",
            video_path=video_path
        )
        print(f"Submission successful! ID: {submission.id}, Status: {submission.status}")
        
        print("\n--- Verifying Duplicate Prevention ---")
        try:
            interview_service.create_submission(
                db=db,
                user=user,
                code_str=code_str,
                topic_taught="Physics",
                video_path=video_path
            )
            print("❌ Error: Duplicate submission was allowed!")
        except Exception as e:
            print(f"✅ Correct: Duplicate submission rejected. ({str(e.detail)})")
            
        print("\nINTERVIEW WORKFLOW VERIFICATION COMPLETE.")
        
    finally:
        print("\n--- Final Cleanup ---")
        # cleanup(db, user_email, code_str)
        db.close()

if __name__ == "__main__":
    test_interview_flow()
