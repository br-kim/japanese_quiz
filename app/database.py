from redis import asyncio as aioredis
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import get_settings
import constants

engine = create_engine(get_settings().DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

redis_connection = aioredis.from_url(constants.REDIS_URL)

Base = declarative_base()
