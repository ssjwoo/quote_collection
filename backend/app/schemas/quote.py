from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional

# 공통
class QuoteBase(BaseModel):
    content: str
    page: Optional[str] = None
    source_id: int
    user_id: int

# 문장 등록
class QuoteCreate(QuoteBase):
    pass

class SourceCreateForQuote(BaseModel):
    title: str
    source_type: str
    creator: str
    publisher_id: Optional[int] = None
    producer_id: Optional[int] = None
    release_year: Optional[int] = None
    isbn: Optional[str] = None

class QuoteCreateWithSource(BaseModel):
    content: str
    page: Optional[str] = None
    user_id: int
    source: SourceCreateForQuote

# 문장 수정
class QuoteUpdate(BaseModel):
    content: Optional[str] = None
    page: Optional[str] = None
    source_id: Optional[int] = None

# DB에서 관리되는 모델
class QuoteInDB(QuoteBase):
    id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True

#클라이언트에게 반환할 모델 -> QuoteInDB 그대로
class QuoteRead(QuoteInDB):
    pass
