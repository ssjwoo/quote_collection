from pydantic import BaseModel, Field
from datetime import datetime, timezone

class BookmarkBase(BaseModel):
    user_id: int
    quote_id: int

class BookmarkCreate(BookmarkBase):
    pass

class BookmarkInDB(BookmarkBase):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True

class BookmarkRead(BookmarkInDB):
    pass
