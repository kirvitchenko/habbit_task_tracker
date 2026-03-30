import celery

from app.core.config import REDIS_HOST, REDIS_PORT, REDIS_BROKER_DB, REDIS_BROKER_DATA_DB

broker_url = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_BROKER_DB}'
result_backend = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_BROKER_DATA_DB}'

celery_app = celery.Celery(broker=broker_url, backend=result_backend)

celery_app.conf.imports = ['app.tasks.notifications']
