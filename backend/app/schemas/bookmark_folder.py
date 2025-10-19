from pydantic import BaseModel

class BookmarkFolderBase(BaseModel):
    name: str
    user_id: int

class BookmarkFolderCreate(BookmarkFolderBase):
    pass

class BookmarkFolderUpdate(BaseModel):
    name: str | None = None

class BookmarkFolderRead(BookmarkFolderBase):
    id: int

    class Config:
        from_attributes = True
