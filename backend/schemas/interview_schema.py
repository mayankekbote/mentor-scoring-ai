from pydantic import BaseModel
from typing import Optional

class CodeValidationRequest(BaseModel):
    code: str

class CodeValidationResponse(BaseModel):
    organization_name: str
    status: str = "valid"

class InterviewSubmissionRequest(BaseModel):
    interview_code: str
    topic_taught: str
    video_path: str

class UploadResponse(BaseModel):
    video_path: str
