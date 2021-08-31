from datetime import datetime

from pydantic import BaseModel


class SubmissionCreate(BaseModel):
    filename: str
    timestamp: datetime
    word_count: int


class SubmissionRow(SubmissionCreate):
    id: int

    class Config:
        # will tell pydantic model to read data even if it is not a dict, but a orm model
        # so id = data["id"] and id = data.id both work
        orm_mode = True
