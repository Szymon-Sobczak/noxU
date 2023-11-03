"""Dependencies module for NoxU API."""

from app.db.database import SessionLocal


def get_db():
    """Yields Database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
