from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.auth import crud, schemas
from app.api.auth.dependencies import get_current_user
from app.core.config import settings
from app.core.security import create_access_token
from app.db.client import client

router = APIRouter()


@router.post("/signup", response_model=schemas.Token)
async def signup(user_create: schemas.UserCreate) -> schemas.Token:
    existing = await crud.get_user_by_email(client, user_create.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = await crud.create_user(client, user_create.email, user_create.password, user_create.name)
    access_token = create_access_token(subject=user.id, expires_delta=timedelta(minutes=settings.access_token_expire_minutes))
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> schemas.Token:
    user = await crud.get_user_by_email(client, form_data.username)
    if not user or not crud.verify_password(form_data.password, user.hashedPassword):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(subject=user.id, expires_delta=timedelta(minutes=settings.access_token_expire_minutes))
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def read_current_user(current_user=Depends(get_current_user)) -> dict:
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "role": current_user.role,
    }
