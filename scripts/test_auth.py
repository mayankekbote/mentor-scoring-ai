import sys
from pathlib import Path
import os
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

# Add project root to sys.path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from backend.database import SessionLocal, engine, Base
from backend.services import auth_service
from backend.schemas.user_schema import UserCreate, UserLogin
from backend.models import User, Admin, PasswordReset

def cleanup_users(db: Session, emails: list):
    """Safely delete users in order to satisfy FK constraints."""
    users = db.query(User).filter(User.email.in_(emails)).all()
    user_ids = [u.id for u in users]
    if user_ids:
        db.query(PasswordReset).filter(PasswordReset.user_id.in_(user_ids)).delete(synchronize_session=False)
        db.query(Admin).filter(Admin.user_id.in_(user_ids)).delete(synchronize_session=False)
        db.query(User).filter(User.id.in_(user_ids)).delete(synchronize_session=False)
    db.commit()

def test_auth_flow():
    db = SessionLocal()
    user_email = "test_candidate@example.com"
    admin_email = "test_admin@example.com"
    
    try:
        print("--- Initial Cleanup ---")
        cleanup_users(db, [user_email, admin_email])
        
        print("\n--- Testing Registration ---")
        user_in = UserCreate(
            name="Test Candidate",
            email=user_email,
            password="testpassword123",
            age=25,
            subject_domain="Computer Science",
            years_experience=2,
            organization="Test University"
        )
        user = auth_service.register_user(db, user_in)
        print(f"Registered user: {user.name} ({user.email})")
        
        print("\n--- Testing Login (Candidate) ---")
        login_in = UserLogin(email=user_email, password="testpassword123")
        login_resp = auth_service.authenticate_user(db, login_in)
        print(f"Login successful. is_admin: {login_resp['user']['is_admin']}")
        
        print("\n--- Testing Admin Detection ---")
        admin_user_in = UserCreate(
            name="Test Admin",
            email=admin_email,
            password="adminpassword",
            organization="HQ"
        )
        admin_user = auth_service.register_user(db, admin_user_in)
        
        # Add to admins table
        admin_entry = Admin(user_id=admin_user.id, organization_name="HQ")
        db.add(admin_entry)
        db.commit()
        
        admin_login_in = UserLogin(email=admin_email, password="adminpassword")
        admin_login_resp = auth_service.authenticate_user(db, admin_login_in)
        print(f"Admin login successful. is_admin: {admin_login_resp['user']['is_admin']}")
        
        print("\n--- Testing Password Reset Flow ---")
        auth_service.request_password_reset(db, user_email)
        reset_entry = db.query(PasswordReset).filter(PasswordReset.user_id == user.id).first()
        print(f"Reset token generated: {reset_entry.token}")
        
        auth_service.reset_password(db, reset_entry.token, "newpassword456")
        print("Password reset successful.")
        
        # Verify login with new password
        new_login_in = UserLogin(email=user_email, password="newpassword456")
        auth_service.authenticate_user(db, new_login_in)
        print("Login with new password successful.")
        print("\nAUTHENTICATION VERIFICATION COMPLETE.")
        
    finally:
        print("\n--- Final Cleanup ---")
        cleanup_users(db, [user_email, admin_email])
        db.close()

if __name__ == "__main__":
    test_auth_flow()
