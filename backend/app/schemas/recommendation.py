from pydantic import BaseModel
from typing import Optional

class RecommendationItem(BaseModel):
    id: int
    content: str
    page: Optional[str] = None
    source_id: int
    source_title: Optional[str] = None
    book_title: Optional[str] = None
    bookmark_count: Optional[int] = None

    model_config = {"from_attributes": True}
