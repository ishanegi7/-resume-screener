from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.assessments import router as assessment_router
from app.api.jobs import router as job_router
from app.api.resumes import router as resume_router
from app.core.config import settings
from app.db.client import client

app = FastAPI(title="Resume Screener API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(job_router, prefix="/api/jobs", tags=["jobs"])
app.include_router(resume_router, prefix="/api/resumes", tags=["resumes"])
app.include_router(assessment_router, prefix="/api/assessments", tags=["assessments"])


@app.on_event("startup")
async def startup() -> None:
    await client.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await client.disconnect()
