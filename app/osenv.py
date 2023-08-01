import os

PORT_NUMBER = int(os.environ.get("PORT", 8000))

GOOGLE_CLIENT_ID = os.getenv('JPN_QUIZ_GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('JPN_QUIZ_GOOGLE_CLIENT_SECRET')

JWT_KEY = os.getenv('JPN_QUIZ_JWT_KEY', "secret-key")
ENVIRON = os.getenv('JPN_QUIZ_ENVIRON', "dev")

if ENVIRON == "test":
    DATABASE_URL = os.getenv('DATABASE_URL', default="postgresql://ii:1234@localhost:5432/test_database")
    SERVER_URL = "http://localhost:8000"
else:
    DATABASE_URL = os.getenv('DATABASE_URL', default="postgresql://ii:1234@localhost:5432/japanese_quiz")
    SERVER_URL = "https://japanese-quiz.site"

if ENVIRON == "local":
    SERVER_URL = "http://localhost:8000"

TEST_DATABASE_URL = os.getenv('TEST_DATABASE_URL', default="postgresql://ii:1234@localhost:5432/test_database")

REDIS_URL = os.getenv("REDIS_URL", default="redis://localhost:6379")

