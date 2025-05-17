from sqlalchemy import create_engine, text
from engine_and_session import sql_connection_string, sql_connection_string_no_database, db_name

test_db_name = db_name + "_test"
sql_connection_string_test = sql_connection_string + "_test"

# Global shared engine for tests
testEngine = create_engine(sql_connection_string_test, echo=True)

def create_db_if_not_exists():
    engine = create_engine(sql_connection_string_no_database, echo=True)
    with engine.connect() as conn:
        try:
            conn.execute(text(f'create database if not exists {test_db_name}'))
        except:
            raise Exception("create database failed...")
    engine.dispose()

def drop_and_recreate_db():
    engine = create_engine(sql_connection_string_no_database, echo=True)
    with engine.connect() as conn:
        try:
            conn.execute(text(f'drop database {test_db_name}'))
        except:
            raise Exception("drop database failed...")
        try:
            conn.execute(text(f'create database {test_db_name}'))
        except:
            raise Exception("create database failed...")
    engine.dispose()