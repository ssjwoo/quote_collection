from pydantic import BaseModel, Field
from datetime import datetime, timezone

class BookmarkBase(BaseModel):
    user_id: int
    quote_id: int

class BookmarkCreate(BookmarkBase):
    quote_data: dict | None = None  # AI 추천 문구 등 DB에 없는 경우를 위한 데이터


class BookmarkInDB(BookmarkBase):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True

class BookmarkRead(BookmarkInDB):
    pass
