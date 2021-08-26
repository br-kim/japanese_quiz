import aioredis
import asyncio
import time
from urllib.parse import urlparse
import osenv

redis_connection = aioredis.from_url(osenv.REDIS_URL)
