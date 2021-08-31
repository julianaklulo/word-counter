from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from app.models import Submission
from app.schemas import SubmissionCreate


def get_submissions(db: Session) -> List[Submission]:
    return db.query(Submission).all()


def get_submissions_by_filename(db: Session, filename: str) -> List[Submission]:
    return db.query(Submission).filter(Submission.filename == filename).all()


def get_submissions_by_date_range(
    db: Session, initial_timestamp: datetime, final_timestamp: datetime
) -> List[Submission]:
    return (
        db.query(Submission)
        .filter(Submission.timestamp.between(initial_timestamp, final_timestamp))
        .all()
    )


def get_submissions_by_filename_and_date_range(
    db: Session, filename: str, initial_timestamp: datetime, final_timestamp: datetime
):
    return (
        db.query(Submission)
        .filter(
            Submission.filename == filename,
            Submission.timestamp.between(initial_timestamp, final_timestamp),
        )
        .all()
    )


def add_submission(db: Session, submission: SubmissionCreate) -> Submission:
    new_submission = Submission(**submission.dict())
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    return new_submission
