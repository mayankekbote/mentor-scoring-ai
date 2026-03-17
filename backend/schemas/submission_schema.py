from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class SubmissionBase(BaseModel):
    interview_code_id: int
    topic_taught: Optional[str] = None

class SubmissionCreate(SubmissionBase):
    video_url: str

class SubmissionResponse(SubmissionBase):
    id: int
    user_id: int
    video_url: str
    followup_answer_url: Optional[str] = None
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
