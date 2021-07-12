from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import osenv


SQLALCHEMY_DATABASE_URL = osenv.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL, encoding='utf8')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
