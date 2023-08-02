import os

PORT_NUMBER: int = int(os.environ.get("PORT", 8000))
REDIS_URL: str = os.getenv("REDIS_URL", default="redis://localhost:6379")
GOOGLE_CLIENT_ID: str = os.getenv('JPN_QUIZ_GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET: str = os.getenv('JPN_QUIZ_GOOGLE_CLIENT_SECRET')
JWT_KEY: str = os.getenv('JPN_QUIZ_JWT_KEY', "secret-key")
TEST_DATABASE_URL: str = os.getenv('TEST_DATABASE_URL', default="postgresql://ii:1234@localhost:5432/test_database")
