import json
from typing import Any

import httpx

from app.core.config import settings

OPENAI_URL = "https://api.openai.com/v1/chat/completions"
MODEL = "gpt-4o-mini"

PROMPT = """You are an AI assistant that compares a resume against a job description.

Provide a JSON object with the following keys:
- overall_score: float between 0 and 100
- skill_score: float between 0 and 100
- experience_score: float between 0 and 100
- education_score: float between 0 and 100
- ats_score: float between 0 and 100
- missing_skills: list of strings
- recommendation: short hiring recommendation
- analysis_json: object containing detailed reasoning

Resume Text:
{resume_text}

Job Description:
{job_text}

Return only valid JSON.
"""


def build_prompt(resume_text: str, job_text: str) -> str:
    return PROMPT.format(resume_text=resume_text, job_text=job_text)


async def assess_resume_to_job(resume_text: str, job_text: str) -> dict[str, Any]:
    if not settings.openai_api_key:
        raise RuntimeError("OpenAI API key is missing")

    prompt = build_prompt(resume_text, job_text)

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            OPENAI_URL,
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": "You are a resume assessment engine."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.0,
            },
            headers={
                "Authorization": f"Bearer {settings.openai_api_key}",
                "Content-Type": "application/json",
            },
        )

    response.raise_for_status()
    payload = response.json()
    text = payload["choices"][0]["message"]["content"]

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeError("OpenAI returned malformed JSON") from exc

    return parsed
