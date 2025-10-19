from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, JSON
from sqlalchemy import func
from app.database import Base

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    source_type = Column(Enum("book", "movie", "drama", "tv", "speech", "other", name="source_type"), nullable=False)
    details_id = Column(Integer, nullable=True)
    creator = Column(String(255), nullable=False)
    publisher_id = Column(Integer, ForeignKey("publishers.id"), nullable=True)
    producer_id = Column(Integer, ForeignKey("producers.id"), nullable=True)
    release_year = Column(Integer, nullable=True)
    isbn = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
