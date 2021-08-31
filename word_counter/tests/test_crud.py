from datetime import datetime

from app import crud
from app.models import Submission


def test_add_submission(session, submission):
    """Test the creation of a word counter submission on the
    database.
    """
    new_submission = crud.add_submission(session, submission)
    assert new_submission.filename == "file1.txt"
    assert new_submission.timestamp == datetime.strptime(
        "2021-08-29T00:00:00", "%Y-%m-%dT%H:%M:%S"
    )
    assert new_submission.word_count == 5


def test_get_submissions(session, submission):
    """Test the retrieve of a word counter submission from the
    database.
    """
    session.add(Submission(**submission.dict()))
    session.commit()

    submissions = crud.get_submissions(session)
    assert len(submissions) == 1
    assert submissions[0].filename == "file1.txt"
    assert submissions[0].timestamp == datetime.strptime(
        "2021-08-29T00:00:00", "%Y-%m-%dT%H:%M:%S"
    )
    assert submissions[0].word_count == 5


def test_get_submissions_by_filename(session, submission):
    """Test the retrieve of word counter submissions from the
    database filtering by filename.
    """
    session.add(Submission(**submission.dict()))

    submission2 = Submission(
        filename="file2.txt",
        timestamp=datetime.strptime("2021-08-29T00:00:00", "%Y-%m-%dT%H:%M:%S"),
        word_count=5,
    )
    session.add(submission2)

    session.commit()

    all_submissions = crud.get_submissions(session)
    filtered_submissions = crud.get_submissions_by_filename(session, "file2.txt")
    assert len(all_submissions) == 2
    assert len(filtered_submissions) == 1
    assert filtered_submissions[0].filename == "file2.txt"


def test_get_submissions_by_date_range(session, submission):
    """Test the retrieve of word counter submissions from the
    database filtering by date range.
    """
    session.add(Submission(**submission.dict()))

    submission2 = Submission(
        filename="file2.txt",
        timestamp=datetime.strptime("2021-08-29T00:30:00", "%Y-%m-%dT%H:%M:%S"),
        word_count=5,
    )
    session.add(submission2)

    submission3 = Submission(
        filename="file3.txt",
        timestamp=datetime.strptime("2021-08-29T00:35:00", "%Y-%m-%dT%H:%M:%S"),
        word_count=5,
    )
    session.add(submission3)

    session.commit()

    all_submissions = crud.get_submissions(session)
    assert len(all_submissions) == 3

    initial_timestamp = datetime.strptime("2021-08-29T00:15:00", "%Y-%m-%dT%H:%M:%S")
    final_timestamp = datetime.strptime("2021-08-29T00:45:00", "%Y-%m-%dT%H:%M:%S")

    filtered_submissions = crud.get_submissions_by_date_range(
        session, initial_timestamp, final_timestamp
    )
    assert len(filtered_submissions) == 2
    assert initial_timestamp <= filtered_submissions[0].timestamp <= final_timestamp
    assert initial_timestamp <= filtered_submissions[1].timestamp <= final_timestamp


def test_get_submissions_by_filename_and_date_range(session, submission):
    """Test the retrieve of word counter submission from the
    database filtering both by filename and date range.
    """
    session.add(Submission(**submission.dict()))

    submission2 = Submission(
        filename="file1.txt",
        timestamp=datetime.strptime("2021-08-29T00:10:00", "%Y-%m-%dT%H:%M:%S"),
        word_count=5,
    )
    session.add(submission2)

    submission3 = Submission(
        filename="file2.txt",
        timestamp=datetime.strptime("2021-08-29T00:10:00", "%Y-%m-%dT%H:%M:%S"),
        word_count=5,
    )
    session.add(submission3)

    session.commit()

    all_submissions = crud.get_submissions(session)
    assert len(all_submissions) == 3

    filename = "file1.txt"
    initial_timestamp = datetime.strptime("2021-08-29T00:00:00", "%Y-%m-%dT%H:%M:%S")
    final_timestamp = datetime.strptime("2021-08-29T00:15:00", "%Y-%m-%dT%H:%M:%S")

    filtered_submissions = crud.get_submissions_by_filename_and_date_range(
        session, filename, initial_timestamp, final_timestamp
    )
    assert len(filtered_submissions) == 2

    assert filtered_submissions[0].filename == "file1.txt"
    assert filtered_submissions[1].filename == "file1.txt"

    assert initial_timestamp <= filtered_submissions[0].timestamp <= final_timestamp
    assert initial_timestamp <= filtered_submissions[1].timestamp <= final_timestamp
