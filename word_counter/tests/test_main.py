from datetime import datetime

from freezegun import freeze_time

from app.main import word_counter


def test_word_counter():
    """
    Test the word counter function to check if return value is
    correct.
    """
    text = "Text file with 5 words"
    word_count = word_counter(text)
    assert word_count == 5


@freeze_time("2021-08-29T00:00:00")
def test_create_submission(client):
    """Test the endpoint that creates a word counter submission."""

    file = {"file": ("file1.txt", "bla")}
    response = client.post("/word-counter", files=file)
    assert response.status_code == 201

    response_data = response.json()

    assert response_data["filename"] == "file1.txt"
    assert response_data["timestamp"] == "2021-08-29T00:00:00"
    assert response_data["word_count"] == 1


@freeze_time("2021-08-29T00:00:00")
def test_read_submissions(client):
    """Test the endpoint that retrieves word counter submissions."""
    file1 = {"file": ("file1.txt", "bla")}
    client.post("/word-counter", files=file1)

    file2 = {"file": ("file2.txt", "bla bla")}
    client.post("/word-counter", files=file2)

    response = client.get("/word-counter")
    assert response.status_code == 200

    submissions = response.json()

    assert len(submissions) == 2
    assert submissions[0]["filename"] == "file1.txt"
    assert submissions[0]["timestamp"] == "2021-08-29T00:00:00"
    assert submissions[0]["word_count"] == 1

    assert submissions[1]["filename"] == "file2.txt"
    assert submissions[1]["timestamp"] == "2021-08-29T00:00:00"
    assert submissions[1]["word_count"] == 2


@freeze_time("2021-08-29T00:30:00")
def test_read_submissions_filter_by_filename(client):
    """Test the endpoint that retrieves word counter submissions
    filtering by filename.
    """
    file1 = {"file": ("file1.txt", "bla")}
    client.post("/word-counter", files=file1)

    file2 = {"file": ("file2.txt", "bla bla")}
    client.post("/word-counter", files=file2)

    response = client.get("/word-counter", params={"filename": "file1.txt"})
    assert response.status_code == 200

    submissions_by_filename = response.json()

    assert len(submissions_by_filename) == 1
    assert submissions_by_filename[0]["filename"] == "file1.txt"


def test_read_submissions_filter_by_date_range(client):
    """Test the endpoint that retrieves word counter submissions filtering
    by date range.
    """
    with freeze_time("2021-08-29T00:15:00"):
        file1 = {"file": ("file1.txt", "bla")}
        client.post("/word-counter", files=file1)

    with freeze_time("2021-08-29T00:20:00"):
        file2 = {"file": ("file2.txt", "bla bla")}
        client.post("/word-counter", files=file2)

    initial_timestamp = "2021-08-29T00:00:00"
    final_timestamp = "2021-08-29T00:19:00"

    response = client.get(
        "/word-counter",
        params={
            "initial_timestamp": initial_timestamp,
            "final_timestamp": final_timestamp,
        },
    )
    assert response.status_code == 200

    submissions_by_date_range = response.json()

    assert len(submissions_by_date_range) == 1

    initial_timestamp = datetime.strptime(initial_timestamp, "%Y-%m-%dT%H:%M:%S")
    final_timestamp = datetime.strptime(final_timestamp, "%Y-%m-%dT%H:%M:%S")

    filtered_submission_timestamp = submissions_by_date_range[0]["timestamp"]
    filtered_submission_timestamp = datetime.strptime(
        filtered_submission_timestamp, "%Y-%m-%dT%H:%M:%S"
    )

    assert initial_timestamp <= filtered_submission_timestamp <= final_timestamp


def test_read_submissions_filter_by_filename_and_date_range(client):
    """Test the endpoint that retrieves word counter submissions filtering
    by filename and date range.
    """
    with freeze_time("2021-08-29T00:15:00"):
        file1 = {"file": ("file1.txt", "bla")}
        client.post("/word-counter", files=file1)

    with freeze_time("2021-08-29T00:20:00"):
        file2 = {"file": ("file2.txt", "bla bla")}
        client.post("/word-counter", files=file2)

    initial_timestamp = "2021-08-29T00:10:00"
    final_timestamp = "2021-08-29T00:30:00"

    response = client.get(
        "/word-counter",
        params={
            "initial_timestamp": initial_timestamp,
            "final_timestamp": final_timestamp,
            "filename": "file2.txt",
        },
    )
    assert response.status_code == 200

    submissions = response.json()

    assert len(submissions) == 1
    assert submissions[0]["filename"] == "file2.txt"

    initial_timestamp = datetime.strptime(initial_timestamp, "%Y-%m-%dT%H:%M:%S")
    final_timestamp = datetime.strptime(final_timestamp, "%Y-%m-%dT%H:%M:%S")

    filtered_submission_timestamp = submissions[0]["timestamp"]
    filtered_submission_timestamp = datetime.strptime(
        filtered_submission_timestamp, "%Y-%m-%dT%H:%M:%S"
    )

    assert initial_timestamp <= filtered_submission_timestamp <= final_timestamp


def test_read_submissions_filter_by_invalid_date_range(client):
    """Test the endpoint that retrieves word counter submissions passing
    an invalid date range for filtering.
    """
    initial_timestamp = "2021-08-29T00:30:00"
    final_timestamp = "2021-08-29T00:10:00"

    response = client.get(
        "/word-counter",
        params={
            "initial_timestamp": initial_timestamp,
            "final_timestamp": final_timestamp,
        },
    )
    assert response.status_code == 400
    response = response.json()
    assert (
        response["detail"] == "Final timestamp must be greater than initial timestamp."
    )


def test_read_submissions_filter_by_missing_date_range(client):
    """Test the endpoint that retrieves word counter submissions
    passing only one timestamp for date range filtering.
    """
    initial_timestamp = "2021-08-29T00:30:00"

    response = client.get(
        "/word-counter",
        params={
            "initial_timestamp": initial_timestamp,
        },
    )
    assert response.status_code == 400
    response = response.json()
    assert (
        response["detail"]
        == "Both initial and final timestamp must be provided to filter by date range."
    )


def test_read_submissions_with_empty_response(client):
    """Test the endpoint that retrieves word counter submissions
    response when there is none submissions to return.
    """
    response = client.get("/word-counter")
    assert response.status_code == 204
    response = response.json()
    assert response["detail"] == "No Content"
