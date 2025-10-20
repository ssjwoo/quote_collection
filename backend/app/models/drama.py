from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Drama(Base):
    __tablename__ = "dramas"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True)
    producer_id = Column(Integer, ForeignKey("producers.id"), nullable=False)
    release_date = Column(Date)

    producer = relationship("Producer")
