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
    database_url = "postgresql://intsea:OceanHides1000Pearls@localhost:5433/intseadb_test"
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
    os.environ["DATABASE_URL"] = "postgresql://intsea:OceanHides1000Pearls@localhost:5433/intseadb_test"
    os.environ["REDIS_URL"] = "redis://localhost:6380"
    os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"
    os.environ["ENVIRONMENT"] = "test"
    os.environ["DEBUG"] = "true"
