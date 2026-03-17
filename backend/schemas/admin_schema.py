from pydantic import BaseModel, ConfigDict
from datetime import datetime

class AdminBase(BaseModel):
    organization_name: str

class AdminCreate(AdminBase):
    user_id: int

class AdminResponse(AdminBase):
    id: int
    user_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AdminCreateRequest(BaseModel):
    name: str
    email: str
    password: str

class AdminDetailResponse(BaseModel):
    id: int
    name: str
    email: str
    organization_name: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class InterviewCallRequest(BaseModel):
    interview_date: str
    interview_time: str
