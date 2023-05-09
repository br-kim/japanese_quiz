import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

import osenv
from models import Base


def create_database():
    engine = create_engine(osenv.POSTGRES_DATABASE_URL)# + "/test_db")
    conn = engine.connect()
    conn.execute(text("commit"))
    try:
        conn.execute(text("CREATE DATABASE test_database"))
    except:
        pass

@pytest.fixture(scope="session")
def session():
    # engine = create_engine(SQLALCHEMY_DATABASE_URL)
    # conn = engine.connect()
    # conn.execute('commit')
    # try:
    #     conn.execute("create database test_db")
    # except:
    #     pass
    # finally:
    #     conn.close()
    create_database()
    engine = create_engine(osenv.TEST_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()

    # engine = create_engine(SQLALCHEMY_DATABASE_URL)
    # conn = engine.connect()
    # conn.execute('commit')
    # conn.execute("drop database test_db with (force)")

