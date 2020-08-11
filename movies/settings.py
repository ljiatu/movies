import os

DB_URL = os.environ.get("DB_URL", "postgresql://localhost/movies")
TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "b6dcd3ce6d71f843e91506c263fa678e")
TMDB_API_HOST = os.environ.get("TMDB_API_HOST", "api.themoviedb.org")
TMDB_API_VERSION = os.environ.get("TMDB_API_VERSION", "3")
TMDB_BASE_URL = os.environ.get(
    "TMDB_BASE_URL", f"https://{TMDB_API_HOST}/{TMDB_API_VERSION}"
)
TMDB_GUEST_SESSION_ID = os.environ.get(
    "TMDB_GUEST_SESSION_ID", "74f31bdc6b3ad840a0dafd22443ce171"
)
