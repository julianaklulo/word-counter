from datetime import datetime
from typing import List, Optional

from fastapi import Depends, FastAPI, File, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import engine, get_session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def word_counter(text: str):
    return len(text.split())


@app.post(
    "/word-counter",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.SubmissionRow,
)
async def create_submission(
    file: UploadFile = File(...), db: Session = Depends(get_session)
):
    file_content = await file.read()

    submission = schemas.SubmissionCreate(
        filename=file.filename,
        timestamp=datetime.now(),
        word_count=word_counter(file_content),
    )

    return crud.add_submission(db, submission)


@app.get("/word-counter", response_model=List[schemas.SubmissionRow])
def read_submissions(
    db: Session = Depends(get_session),
    filename: Optional[str] = Query(
        None, max_length=255, description="String to filter submissions by filename"
    ),
    initial_timestamp: Optional[datetime] = Query(
        None, description="Initial timestamp to filter submissions by date range"
    ),
    final_timestamp: Optional[datetime] = Query(
        None, description="Final timestamp to filter submissions by date range"
    ),
):
    if initial_timestamp and final_timestamp:
        if initial_timestamp > final_timestamp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Final timestamp must be greater than initial timestamp.",
            )

    if (initial_timestamp and not final_timestamp) or (
        final_timestamp and not initial_timestamp
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both initial and final timestamp must be provided to filter by date range.",
        )

    if filename and not (initial_timestamp and final_timestamp):
        submissions = crud.get_submissions_by_filename(db, filename)

    elif (initial_timestamp and final_timestamp) and not filename:
        submissions = crud.get_submissions_by_date_range(
            db, initial_timestamp, final_timestamp
        )

    elif filename and initial_timestamp and final_timestamp:
        submissions = crud.get_submissions_by_filename_and_date_range(
            db, filename, initial_timestamp, final_timestamp
        )

    else:
        submissions = crud.get_submissions(db)

    if not submissions:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

    return submissions
