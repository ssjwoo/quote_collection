from pydantic import BaseModel
from typing import List, Union
from .quote import QuoteRead
from .source import SourceRead
from .tag import TagRead

class SearchResult(BaseModel):
    quotes: List[QuoteRead]
    sources: List[SourceRead]
    tags: List[TagRead]
