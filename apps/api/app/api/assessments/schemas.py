from typing import Any

from pydantic import BaseModel

class AssessmentRequest(BaseModel):
    resume_id: str
    job_description_id: str

class AssessmentResult(BaseModel):
    overall_score: float
    skill_score: float
    experience_score: float
    education_score: float
    ats_score: float
    missing_skills: list[str]
    recommendation: str
    analysis_json: dict[str, Any]

class AssessmentResponse(AssessmentResult):
    id: str
    resume_id: str
    job_description_id: str
    created_at: str
