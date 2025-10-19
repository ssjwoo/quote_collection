from pydantic import BaseModel, Field
from datetime import datetime, timezone

# 공통
class TagBase(BaseModel):
    name: str

# 생성
class TagCreate(TagBase):
    pass

# 수정
class TagUpdate(BaseModel):
    name: str | None = None

# DB에서 관리되는 모델
class TagInDB(TagBase):
    id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        from_attributes = True

# 클라이언트에게 반환할 모델 -> TagInDB 그대로
class TagRead(TagInDB):
    pass
