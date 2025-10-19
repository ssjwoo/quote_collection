from pydantic import BaseModel, Field
from datetime import date

# 기본 Movie 스키마
class MovieBase(BaseModel):
    title: str = Field(..., max_length=100)
    director: str = Field(..., max_length=50)
    release_date: date | None = None

# Movie 생성을 위한 스키마
class MovieCreate(MovieBase):
    pass

# Movie 수정을 위한 스키마
class MovieUpdate(BaseModel):
    title: str | None = None
    director: str | None = None
    release_date: date | None = None

# DB에서 읽어올 때 사용할 스키마
class MovieRead(MovieBase):
    id: int

    class Config:
        from_attributes = True # SQLAlchemy 모델을 Pydantic 모델로 변환