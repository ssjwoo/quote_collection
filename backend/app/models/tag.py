# NOTE: The frontend uses a pre-determined set of tags (e.g., radio buttons).
# The data in this table should be considered static and pre-populated.

from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

from .quote_tag import quote_tags
from .movie import movie_tag_association

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)

    quotes = relationship("Quote", secondary=quote_tags, back_populates="tags")

    ### Movie와의 다대다 관계 설정 ###
    movies = relationship(
        "Movie",
        secondary=movie_tag_association,
        back_populates="tags"
    )
