from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.auth.dependencies import get_current_user
from app.api.jobs.schemas import JobDescriptionCreate, JobDescriptionResponse
from app.db.client import client

router = APIRouter()


@router.post("/", response_model=JobDescriptionResponse)
async def create_job_description(
    payload: JobDescriptionCreate,
    current_user=Depends(get_current_user),
) -> JobDescriptionResponse:
    job = await client.jobDescription.create(
        data={
            "title": payload.title,
            "description": payload.description,
            "rawText": payload.description,
            "createdBy": {"connect": {"id": current_user.id}},
            "organization": {"connect": {"id": current_user.organizationId}},
        }
    )
    return JobDescriptionResponse(
        id=job.id,
        title=job.title,
        description=job.description,
        raw_text=job.rawText,
        created_at=job.createdAt.isoformat(),
    )


@router.get("/{job_id}", response_model=JobDescriptionResponse)
async def get_job_description(job_id: str, current_user=Depends(get_current_user)) -> JobDescriptionResponse:
    job = await client.jobDescription.find_unique(where={"id": job_id})

    if not job or job.organizationId != current_user.organizationId:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job description not found")

    return JobDescriptionResponse(
        id=job.id,
        title=job.title,
        description=job.description,
        raw_text=job.rawText,
        created_at=job.createdAt.isoformat(),
    )
