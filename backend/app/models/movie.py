from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

# Movie와 Tag의 다대다 관계를 위한 연결 테이블
movie_tag_association = Table(
    'movie_tag', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True)
    director = Column(String(50), nullable=False)
    release_date = Column(Date)

    # Movie와 Tag는 다대다 관계
    tags = relationship(
        "Tag",
        secondary=movie_tag_association,
        back_populates="movies"
    )