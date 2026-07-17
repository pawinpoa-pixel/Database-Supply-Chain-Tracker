import os
from pathlib import Path

import uvicorn
from sqlalchemy import text

# Importing main creates SQLAlchemy tables and applies the repository migrations.
from main import app
from database import engine


SEED_FILE = Path(__file__).resolve().parent.parent / "sql" / "render_seed.sql"
SEED_LOCK_ID = 2026071701


def seed_demo_data() -> None:
    enabled = os.getenv("SEED_DEMO_DATA", "true").strip().lower()
    if enabled not in {"1", "true", "yes", "on"}:
        print("Demo-data seeding disabled.")
        return

    raw_connection = engine.raw_connection()
    try:
        cursor = raw_connection.cursor()
        cursor.execute("SELECT pg_advisory_lock(%s)", (SEED_LOCK_ID,))
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]

        if user_count == 0:
            print(f"Loading demo data from {SEED_FILE}")
            cursor.execute(SEED_FILE.read_text(encoding="utf-8"))
            raw_connection.commit()
            print("Demo data loaded.")
        else:
            raw_connection.commit()
            print(f"Seed skipped: users table already contains {user_count} row(s).")
    except Exception:
        raw_connection.rollback()
        raise
    finally:
        try:
            cursor = raw_connection.cursor()
            cursor.execute("SELECT pg_advisory_unlock(%s)", (SEED_LOCK_ID,))
            raw_connection.commit()
        except Exception:
            raw_connection.rollback()
        raw_connection.close()


if __name__ == "__main__":
    seed_demo_data()
    uvicorn.run(app, host="127.0.0.1", port=8000, proxy_headers=True)
