from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    age = Column(Integer)
    subject_domain = Column(String)
    resume_url = Column(String)
    years_experience = Column(Integer)
    organization = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    admin_profile = relationship("Admin", back_populates="user", uselist=False)
    submissions = relationship("Submission", back_populates="user")
    password_resets = relationship("PasswordReset", back_populates="user")
