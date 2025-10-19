from sqlalchemy import Column, Integer, String, DateTime, TEXT, ForeignKey
from sqlalchemy import func
from app.database import Base  
from sqlalchemy.orm import relationship

from .quote_tag import quote_tags

class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    content = Column(TEXT, nullable=False)
    page = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    tags = relationship("Tag", secondary=quote_tags, back_populates="quotes")
    source = relationship("Source")