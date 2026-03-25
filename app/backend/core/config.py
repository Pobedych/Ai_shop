import os
from decouple import config

DB_HOST = config("DB_HOST", "localhost")
DB_PORT = config("DB_PORT", "5432")
DB_NAME = config("DB_NAME", "ai_shop")
DB_USER = config("DB_USER", "postgres")
DB_PASSWORD = config("DB_PASSWORD", "postgres")

DATABASE_URL = config(
    "DATABASE_URL",
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)

TG_CHANNEL = config("TG_CHANNEL", "@your_channel")
SUPPORT_ACCOUNT = config("SUPPORT_ACCOUNT", "@support")
"""
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

JWT_SECRET = os.getenv("RANDOM_SECRET", "dev-secret")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_SECONDS = 3600

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_FULLNAME = os.getenv("ADMIN_FULLNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")"""
