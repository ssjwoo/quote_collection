from pydantic import BaseModel


class PopularQuoteResponse(BaseModel):
    title: str
    content: str
    creator: str
