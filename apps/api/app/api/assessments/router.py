from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.assessments.schemas import AssessmentRequest, AssessmentResponse
from app.api.auth.dependencies import get_current_user
from app.db.client import client
from app.services.matching import assess_resume_to_job

router = APIRouter()


@router.post("/", response_model=AssessmentResponse)
async def create_assessment(
    payload: AssessmentRequest,
    current_user=Depends(get_current_user),
) -> AssessmentResponse:
    resume = await client.resume.find_unique(where={"id": payload.resume_id})
    if not resume or resume.organizationId != current_user.organizationId:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

    job = await client.jobDescription.find_unique(where={"id": payload.job_description_id})
    if not job or job.organizationId != current_user.organizationId:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job description not found")

    section = await client.resumeSection.find_first(where={"resumeId": resume.id})
    if not section:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resume text not available")

    assessment = await assess_resume_to_job(
        resume_text=section.content,
        job_text=job.rawText,
    )

    record = await client.resumeAnalysis.create(
        data={
            "resume": {"connect": {"id": resume.id}},
            "jobDescription": {"connect": {"id": job.id}},
            "scoreOverall": assessment["overall_score"],
            "scoreSkills": assessment["skill_score"],
            "scoreExperience": assessment["experience_score"],
            "scoreEducation": assessment["education_score"],
            "scoreATS": assessment["ats_score"],
            "recommendation": assessment["recommendation"],
            "missingSkills": assessment["missing_skills"],
            "analysisJson": assessment["analysis_json"],
        }
    )

    return AssessmentResponse(
        id=record.id,
        resume_id=resume.id,
        job_description_id=job.id,
        overall_score=record.scoreOverall,
        skill_score=record.scoreSkills,
        experience_score=record.scoreExperience,
        education_score=record.scoreEducation,
        ats_score=record.scoreATS,
        missing_skills=record.missingSkills,
        recommendation=record.recommendation,
        analysis_json=record.analysisJson,
        created_at=record.createdAt.isoformat(),
    )
