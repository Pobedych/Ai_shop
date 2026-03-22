import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "ai_shop")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)

TG_CHANNEL = os.getenv("TG_CHANNEL", "@your_channel")
SUPPORT_ACCOUNT = os.getenv("SUPPORT_ACCOUNT", "@support")
"""
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

JWT_SECRET = os.getenv("RANDOM_SECRET", "dev-secret")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_SECONDS = 3600

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_FULLNAME = os.getenv("ADMIN_FULLNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")"""
