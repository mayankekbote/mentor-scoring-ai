from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    interview_code_id = Column(Integer, ForeignKey("interview_codes.id"), nullable=False)
    topic_taught = Column(String)
    video_url = Column(String, nullable=False)
    followup_answer_url = Column(String)
    status = Column(String, default="uploaded") # uploaded / processing / completed / failed
    processing_progress = Column(Float, default=0.0)
    processing_message = Column(String, default="Starting...")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="submissions")
    interview_code = relationship("InterviewCode", back_populates="submissions")
    ai_result = relationship("AIResult", back_populates="submission", uselist=False)

    # Restriction: A candidate can submit only one interview per interview code
    __table_args__ = (
        UniqueConstraint('user_id', 'interview_code_id', name='_user_interview_code_uc'),
    )
