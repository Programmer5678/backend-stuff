from sqlalchemy.orm import Session
from tests.db_utils import testEngine

def override_get_session():
    s = Session(bind=testEngine)
    try:
        yield s
    finally:
        s.close()
