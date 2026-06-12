from pathlib import Path
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    database_url: str = Field(..., env="DATABASE_URL")
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field("HS256", env="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(60, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    openai_api_key: str | None = Field(None, env="OPENAI_API_KEY")
    s3_bucket: str | None = Field(None, env="S3_BUCKET")
    s3_endpoint: str | None = Field(None, env="S3_ENDPOINT")
    s3_access_key: str | None = Field(None, env="S3_ACCESS_KEY")
    s3_secret_key: str | None = Field(None, env="S3_SECRET_KEY")

    class Config:
        env_file = Path(__file__).resolve().parents[2] / ".env"
        env_file_encoding = "utf-8"

settings = Settings()
