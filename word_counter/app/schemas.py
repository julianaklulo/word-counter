from datetime import datetime

from pydantic import BaseModel


class SubmissionCreate(BaseModel):
    filename: str
    timestamp: datetime
    word_count: int


class SubmissionRow(SubmissionCreate):
    id: int

    class Config:
        orm_mode = True
