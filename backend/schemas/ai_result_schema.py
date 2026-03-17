from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Any

class AIResultBase(BaseModel):
    submission_id: int
    score: Optional[float] = None
    strengths: Optional[Any] = None
    weaknesses: Optional[Any] = None
    summary: Optional[str] = None
    transcript: Optional[str] = None
    audio_metrics: Optional[Any] = None
    posture_metrics: Optional[Any] = None

class AIResultCreate(AIResultBase):
    pass

class AIResultResponse(AIResultBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
