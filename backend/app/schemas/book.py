from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional

class BookBase(BaseModel):
    title: str = Field(min_length=1)
    author: str
    publisher: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = None
    publisher: Optional[str] = None

class BookInDB(BookBase):
    id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True

class BookRead(BookInDB):
    pass
