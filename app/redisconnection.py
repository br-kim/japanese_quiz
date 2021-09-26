import aioredis

import osenv

redis_connection = aioredis.from_url(osenv.REDIS_URL)
