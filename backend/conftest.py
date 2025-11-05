import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic import command
from alembic.config import Config

# Set test environment
os.environ["ENVIRONMENT"] = "test"

@pytest.fixture(scope="session")
def test_db_engine():
    """Create test database engine"""
    # Use environment variable if set (for CI), otherwise use local default
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://intsea:OceanHides1000Pearls@localhost:5433/intseadb_test"
    )
    engine = create_engine(database_url)
    
    # Run migrations to set up test database
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("script_location", "alembic")
    command.upgrade(alembic_cfg, "head")
    
    yield engine
    
    # Clean up
    engine.dispose()

@pytest.fixture(scope="function")
def test_db_session(test_db_engine):
    """Create test database session"""
    Session = sessionmaker(bind=test_db_engine)
    session = Session()
    
    yield session
    
    # Rollback and close session
    session.rollback()
    session.close()

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment variables"""
    # Only set if not already set (allows CI to override)
    if "DATABASE_URL" not in os.environ:
        os.environ["DATABASE_URL"] = "postgresql://intsea:OceanHides1000Pearls@localhost:5433/intseadb_test"
    if "REDIS_URL" not in os.environ:
        os.environ["REDIS_URL"] = "redis://localhost:6380"
    if "SECRET_KEY" not in os.environ:
        os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"
    os.environ["ENVIRONMENT"] = "test"
    os.environ["DEBUG"] = "true"
