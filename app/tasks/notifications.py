import logging

from celery_app import celery_app

logger = logging.getLogger(__name__)

handler = logging.FileHandler('app/logs/notifications.log')
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


@celery_app.task
def status_change_task(task_name: str, status: str):
    logger.info(f'Notification: {task_name} changed status to {status}')
