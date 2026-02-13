import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from be_task_ca.database import Base

# Ensure model tables are registered on Base metadata
from be_task_ca.item import model as _item_model  # noqa: F401
from be_task_ca.user import model as _user_model  # noqa: F401


def _create_test_session():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return TestingSessionLocal()


@pytest.fixture
def db_session():
    db = _create_test_session()
    try:
        yield db
    finally:
        db.close()
