from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class InterviewCodeBase(BaseModel):
    code: str
    organization_name: str
    max_attempts: int = 1
    expiry_date: Optional[datetime] = None

class InterviewCodeCreateRequest(BaseModel):
    max_attempts: int
    expiry_date: datetime

class InterviewCodeResponse(InterviewCodeBase):
    id: int
    created_by_admin: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
