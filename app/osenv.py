import os

PORT_NUMBER = int(os.environ.get("PORT", 8000))

GOOGLE_CLIENT_ID = os.getenv('JPN_QUIZ_GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('JPN_QUIZ_GOOGLE_CLIENT_SECRET')

SESSION_KEY = os.getenv('JPN_QUIZ_SESSION_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

