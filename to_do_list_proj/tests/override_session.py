from sqlalchemy.orm import Session
from tests.db_utils import testEngine

def override_get_session():
    
    """
    Dependency override for get_session.
    Yields a SQLAlchemy session bound to the in-memory test database.
    Use in test setup: app.dependency_overrides[get_session] = override_get_session
    """
    
    s = Session(bind=testEngine)
    try:
        yield s
    finally:
        s.close()
