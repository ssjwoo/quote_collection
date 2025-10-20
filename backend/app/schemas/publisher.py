from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional

class PublisherBase(BaseModel):
    name: str
    address: Optional[str] = None

class PublisherCreate(PublisherBase):
    pass

class PublisherUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None

class PublisherInDB(PublisherBase):
    publisher_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True

class PublisherRead(PublisherInDB):
    pass
