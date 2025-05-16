import pytest
from sqlalchemy.orm import Session
from base_for_tables import Base
from app import app
from engine_and_session import get_session
from tests.db_utils import create_db_if_not_exists, drop_and_recreate_db, testEngine
from tests.override_session import override_get_session
from fastapi.testclient import TestClient
from app import app

create_db_if_not_exists()
# Set dependency override
app.dependency_overrides[get_session] = override_get_session

@pytest.fixture
def session():
    drop_and_recreate_db()
    Base.metadata.create_all(testEngine)
    s = Session(bind=testEngine)
    try:
        yield s
    except:
        raise Exception("session create failed!")
    finally:
        s.close()
        testEngine.dispose()

@pytest.fixture
def client(session): 
    return TestClient(app)