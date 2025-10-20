from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional, Dict, Any, Union

from .book import BookRead
from .movie import MovieRead
from .drama import DramaRead

class SourceBase(BaseModel):
    title: str
    source_type: str
    creator: str
    details_id: Optional[int] = None
    producer_id: Optional[int] = None
    publisher_id: Optional[int] = None
    release_year: Optional[int] = None
    isbn: Optional[str] = None

class SourceCreate(SourceBase):
    pass

class SourceUpdate(BaseModel):
    title: Optional[str] = None
    source_type: Optional[str] = None
    creator: Optional[str] = None
    details_id: Optional[int] = None
    producer_id: Optional[int] = None
    publisher_id: Optional[int] = None
    release_year: Optional[int] = None
    isbn: Optional[str] = None

class SourceInDB(SourceBase):
    id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True

class SourceRead(SourceInDB):
    details: Union[BookRead, MovieRead, DramaRead, None] = None
