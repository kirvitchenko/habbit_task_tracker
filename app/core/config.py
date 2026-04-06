"""Config file for project"""

import os
from pathlib import Path
from dotenv import load_dotenv

ENV_FILE = Path(__file__).parent.parent.parent / ".env"
load_dotenv(ENV_FILE)

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

REDIS_BROKER_DATA_DB = os.getenv("REDIS_BROKER_DATA_DB")
REDIS_BROKER_DB = os.getenv("REDIS_BROKER_DB")
REDIS_CACHE_DB = os.getenv("REDIS_CACHE_DB")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

KAFKA_HOST = os.getenv("KAFKA_HOST")
KAFKA_PORT = os.getenv("KAFKA_PORT")

CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST")
CLICKHOUSE_PORT = os.getenv("CLICKHOUSE_PORT")
CLICKHOUSE_USER = os.getenv('CLICKHOUSE_USER')
CLICKHOUSE_PASSWORD = os.getenv('CLICKHOUSE_PASSWORD')

DB_SYNC_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

DB_ASYNC_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
