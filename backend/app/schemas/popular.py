from pydantic import BaseModel


class PopularQuoteResponse(BaseModel):
    id: int
    title: str
    content: str
    creator: str
