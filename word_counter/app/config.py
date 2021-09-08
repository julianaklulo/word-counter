from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    DATABASE_URL: str = Field("sqlite:///./word-count.db")
    TEST_DATABASE_URL: str = Field("sqlite:///./word-count-test.db")

    class Config:
        env_file = ".env"


settings = Settings()
