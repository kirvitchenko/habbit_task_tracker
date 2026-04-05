import logging
from pathlib import Path

from celery_app import celery_app

logger = logging.getLogger(__name__)
log_dir = Path("app/logs")
if not log_dir:
    log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "notifications.log"

handler = logging.FileHandler(log_file)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


@celery_app.task
def status_change_task(task_name: str, status: str):
    logger.info(f"Notification: {task_name} changed status to {status}")
