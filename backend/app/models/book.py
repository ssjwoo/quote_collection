from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import relationship
from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    isbn = Column(String(255), nullable=True)
    publisher_id = Column(Integer, ForeignKey("publishers.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    publisher = relationship("Publisher", backref="books")
