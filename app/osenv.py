import os

PORT_NUMBER = int(os.environ.get("PORT", 8000))

GOOGLE_CLIENT_ID = os.getenv('JPN_QUIZ_GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('JPN_QUIZ_GOOGLE_CLIENT_SECRET')

JWT_KEY = os.getenv('JPN_QUIZ_JWT_KEY', "secret-key")
DATABASE_URL = os.getenv('DATABASE_URL')

REDIS_TLS_URL = os.getenv('REDIS_TLS_URL')
REDIS_URL = os.getenv('REDIS_URL')
