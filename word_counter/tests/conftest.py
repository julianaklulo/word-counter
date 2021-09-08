from datetime import datetime

from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session

from app import schemas
from app.config import settings
from app.database import Base
from app.main import app, get_session


@fixture(scope="session")
def engine():
    return create_engine(
        settings.TEST_DATABASE_URL, connect_args={"check_same_thread": False}
    )


@fixture(scope="session")
def create_tables(engine):
    Base.metadata.create_all(bind=engine)


@fixture
def session(engine, create_tables):
    connection = engine.connect()
    transaction = connection.begin()
    db = Session(bind=connection)
    yield db
    db.close()
    transaction.rollback()
    connection.close()


@fixture
def client(session):
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)


@fixture
def submission():
    return schemas.SubmissionCreate(
        filename="file1.txt",
        timestamp=datetime.strptime("2021-08-29T00:00:00", "%Y-%m-%dT%H:%M:%S"),
        word_count=5,
    )


@fixture
def another_submission():
    return schemas.SubmissionCreate(
        filename="file2.txt",
        timestamp=datetime.strptime("2021-08-29T00:10:00", "%Y-%m-%dT%H:%M:%S"),
        word_count=3,
    )
