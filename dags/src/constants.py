import os

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

BASE_API_URL = "https://livescore-api.com/api-client/scores"
LIVE_SCORES_URL = f"{BASE_API_URL}/live.json?key={API_KEY}&secret={API_SECRET}"
BASE_MATCH_EVENTS_URL = (
    f"{BASE_API_URL}/events.json?key={API_KEY}&secret={API_SECRET}&id="
)

TABLE_NAME = "postgres_db"
POSTGRES_DB_URI = f"postgresql+psycopg2://postgres:postgres@postgres-db/{TABLE_NAME}"
