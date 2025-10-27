from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional

class PublisherBase(BaseModel):
    name: str

class PublisherCreate(PublisherBase):
    pass

class PublisherUpdate(BaseModel):
    name: Optional[str] = None

class PublisherInDB(PublisherBase):
    id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True

class PublisherRead(PublisherInDB):
    pass
