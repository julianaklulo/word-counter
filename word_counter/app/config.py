from prettyconf import config


class Settings:
    DATABASE_URL = config("DATABASE_URL", default="sqlite:///./word-count.db")
    TEST_DATABASE_URL = config(
        "TEST_DATABASE_URL", default="sqlite:///./word-count-test.db"
    )


settings = Settings()
