from datetime import datetime
from pydantic import BaseModel

class ResumeUploadResponse(BaseModel):
    resume_id: str
    file_name: str
    status: str
    uploaded_at: datetime
