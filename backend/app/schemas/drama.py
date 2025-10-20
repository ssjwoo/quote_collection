from pydantic import BaseModel
from datetime import date

class DramaBase(BaseModel):
    title: str
    producer_id: int
    release_date: date | None = None

class DramaCreate(DramaBase):
    pass

class DramaUpdate(BaseModel):
    title: str | None = None
    producer_id: int | None = None
    release_date: date | None = None

class DramaRead(DramaBase):
    id: int

    class Config:
        from_attributes = True
