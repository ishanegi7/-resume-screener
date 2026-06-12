from pydantic import BaseModel

class JobDescriptionCreate(BaseModel):
    title: str
    description: str

class JobDescriptionResponse(BaseModel):
    id: str
    title: str
    description: str
    raw_text: str
    created_at: str
