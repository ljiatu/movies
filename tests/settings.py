import os

TEST_DB_URL = os.environ.get(
    "TEST_DB_URL", "postgresql://postgres@localhost/movies_test"
)
