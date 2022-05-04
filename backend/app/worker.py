from random import randint
from time import sleep
from celery import Celery
from celery.utils.log import get_task_logger
from app.config import settings

celery = Celery('tasks', broker=settings.broker_url, backend=settings.result_backend)
# Create a logger - Enable to display the message on the task logger
celery_log = get_task_logger(__name__)


@celery.task
def my_delay_task(name, num):
    r = randint(1, 100)
    sleep(r)

    celery_log.info(f"Task Complete!")
    return {"message": f"Hi {name}! Your number is {num} im multiple universe"}
