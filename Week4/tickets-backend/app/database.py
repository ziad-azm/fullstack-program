import psycopg

from .config import DATABASE_URL


def get_connection():
    return psycopg.connect(DATABASE_URL)


def init_db() -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS tickets (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(150) NOT NULL,
                    description TEXT,
                    status VARCHAR(20) NOT NULL DEFAULT 'open',
                    priority VARCHAR(20) NOT NULL DEFAULT 'medium',
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                )
                """
            )
