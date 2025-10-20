from pydantic import BaseModel

# 공통
class QuoteTagBase(BaseModel):
    quote_id: int
    tag_id: int

# 추가
class QuoteTagCreate(QuoteTagBase):
    pass

# DB 모델
class QuoteTagInDB(QuoteTagBase):
    class Config:
        from_attributes = True

# 클라이언트에게 반환할 모델 -> QuoteTagInDB 그대로
class QuoteTagRead(QuoteTagInDB):
    pass
