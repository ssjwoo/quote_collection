from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional
from app.schemas.publisher import PublisherRead

class BookBase(BaseModel):
    title: str = Field(min_length=1)
    author: str
    publisher_id: Optional[int] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = None
    publisher_id: Optional[int] = None

class BookInDB(BookBase):
    id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True

class BookRead(BookInDB):
    publisher: Optional[PublisherRead] = None
