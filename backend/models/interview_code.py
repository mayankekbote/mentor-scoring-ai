from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base

class InterviewCode(Base):
    __tablename__ = "interview_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    organization_name = Column(String, nullable=False)
    created_by_admin = Column(Integer, ForeignKey("admins.id"), nullable=False)
    max_attempts = Column(Integer, default=1)
    expiry_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    creator_admin = relationship("Admin", back_populates="interview_codes")
    submissions = relationship("Submission", back_populates="interview_code")
