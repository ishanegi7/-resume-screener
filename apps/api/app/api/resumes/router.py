import os
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from app.api.auth.dependencies import get_current_user
from app.api.resumes.schemas import ResumeUploadResponse
from app.core.config import settings
from app.db.client import client
from app.services.resume_extraction import extract_text_from_pdf

router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "../../../uploads")
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF files are supported")

    resume_id = str(uuid.uuid4())
    file_name = f"{resume_id}.pdf"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    resume = await client.resume.create(
        data={
            "id": resume_id,
            "candidate": {"create": {"name": current_user.name or "Unnamed Candidate"}},
            "organization": {"connect": {"id": current_user.organizationId}},
            "uploadedBy": {"connect": {"id": current_user.id}},
            "filePath": file_path,
            "fileName": file.filename,
            "status": "PENDING",
        }
    )

    extracted_text = await extract_text_from_pdf(file_path)
    await client.resumeSection.create(
        data={
            "resume": {"connect": {"id": resume.id}},
            "sectionType": "OTHER",
            "content": extracted_text,
            "extractedJson": {},
        }
    )

    await client.resume.update(
        where={"id": resume.id},
        data={"status": "PARSED", "parsedAt": datetime.utcnow()},
    )

    return ResumeUploadResponse(
        resume_id=resume.id,
        file_name=file.filename,
        status=resume.status,
        uploaded_at=resume.createdAt.isoformat(),
    )
