"""Pytest fixtures and database test environment setup."""
import pytest
from app.database import engine, Base, SessionLocal
from app.services.ingestion_pipeline import seed_baseline_if_empty

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Ensure tables exist and baseline records are seeded for integration tests."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_baseline_if_empty(db)
    finally:
        db.close()
    yield
