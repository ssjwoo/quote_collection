from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os
import sys


class Settings(BaseSettings):
    TESTING: bool = Field(False, alias="TESTING")
    # 비동기 DB URL
    database_url: str = Field(..., alias="DATABASE_URL")

    # 동기 DB URL
    sync_database_url: str = Field(..., alias="SYNC_DATABASE_URL")

    # Google Vertex AI 설정
    google_project_id: str = Field(..., alias="GOOGLE_PROJECT_ID")
    google_location: str = Field("us-central1", alias="GOOGLE_LOCATION")
    google_application_credentials: str | None = Field(None, alias="GOOGLE_APPLICATION_CREDENTIALS")
    
    # Aladin API 설정
    aladin_api_key: str = Field("", alias="ALADIN_API_KEY")

    secret_key: str = Field(..., alias="SECRET_KEY")
    jwt_algo: str = Field("HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(
        30, alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )  # 30분

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), ".env"),
        case_sensitive=True,
        extra="allow",
        populate_by_name=True
    )

class TestSettings(Settings):
    model_config = SettingsConfigDict(env_file=".env.test")


settings = TestSettings() if Settings().TESTING else Settings()

if settings.google_application_credentials:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials
