from sqlalchemy import Column, DateTime, Integer, String

from app.database import Base


class Submission(Base):
    __tablename__ = "submission"
    id = Column(Integer, primary_key=True)
    filename = Column(String(length=255), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    word_count = Column(Integer)
