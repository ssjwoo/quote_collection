from pydantic import BaseModel, Field
from datetime import date
from typing import List

# 기본 Movie 스키마
class MovieBase(BaseModel):
    title: str = Field(..., max_length=100)
    director: str = Field(..., max_length=50)
    release_date: date | None = None

# 프론트엔드에서 데이터를 받을 때 사용할 스키마
class MovieCreate(MovieBase):
    # '기록하고 싶은 대사'와 '태그' 필드 추가
    quote_content: str = Field(..., max_length=1000)
    tags: List[str] # 태그 이름을 리스트로 받음

# DB에 저장된 후 프론트엔드로 응답을 보낼 때 사용할 스키마
class MovieRead(MovieBase):
    id: int

    class Config:
        from_attributes = True # SQLAlchemy 모델을 Pydantic 모델로 변환