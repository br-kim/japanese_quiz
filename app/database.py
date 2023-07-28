from redis import asyncio as aioredis
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import osenv


SQLALCHEMY_DATABASE_URL = osenv.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

redis_connection = aioredis.from_url(osenv.REDIS_URL)

Base = declarative_base()
