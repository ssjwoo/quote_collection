from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    TESTING: bool = Field(False, alias="TESTING")
    # 비동기 DB URL
    database_url: str = Field(..., alias="DATABASE_URL")

    # 동기 DB URL
    sync_database_url: str = Field(..., alias="SYNC_DATABASE_URL")

    secret_key: str = Field(..., alias="SECRET_KEY")
    jwt_algo: str = Field("HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(
        30, alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )  # 30분

    class Config:
        case_sensitive = True
        extra = "allow"
        populate_by_name = True
        env_file = ".env.dev"

class TestSettings(Settings):
    class Config:
        env_file = ".env.test"


settings = TestSettings() if Settings().TESTING else Settings()
