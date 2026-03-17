from datetime import datetime, timedelta, timezone
import secrets
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.models.user import User
from backend.models.admin import Admin
from backend.models.password_reset import PasswordReset
from backend.schemas.user_schema import UserCreate, UserLogin
from backend.utils.security import hash_password, verify_password, create_access_token
from backend.utils.email_service import send_reset_password_email

def register_user(db: Session, user_in: UserCreate) -> User:
    # Check if user already exists
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = hash_password(user_in.password)
    db_user = User(
        name=user_in.name,
        email=user_in.email,
        password_hash=hashed_password,
        age=user_in.age,
        subject_domain=user_in.subject_domain,
        years_experience=user_in.years_experience,
        organization=user_in.organization,
        resume_url=user_in.resume_url
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, login_in: UserLogin) -> dict:
    user = db.query(User).filter(User.email == login_in.email).first()
    if not user or not verify_password(login_in.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Check if user is admin
    admin = db.query(Admin).filter(Admin.user_id == user.id).first()
    is_admin = admin is not None
    
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "is_admin": is_admin
        }
    }

def request_password_reset(db: Session, email: str) -> bool:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        # We return True anyway to avoid email enumeration
        return True
    
    # Simple secure token
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)
    
    db_reset = PasswordReset(
        user_id=user.id,
        token=token,
        expires_at=expires_at
    )
    db.add(db_reset)
    db.commit()
    
    # Send real email
    send_reset_password_email(email, token)
    
    return True

def reset_password(db: Session, token: str, new_password: str) -> bool:
    reset_entry = db.query(PasswordReset).filter(
        PasswordReset.token == token,
        PasswordReset.expires_at > datetime.now(timezone.utc)
    ).first()
    
    if not reset_entry:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    user = db.query(User).filter(User.id == reset_entry.user_id).first()
    if not user:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
         
    user.password_hash = hash_password(new_password)
    db.delete(reset_entry)
    db.commit()
    return True
