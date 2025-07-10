
from celery import Celery
from celery.schedules import crontab
import redis

celery = Celery('tasks', broker='redis://localhost:6379/0')

r = redis.Redis(host='localhost', port=6379, db=0)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, ping.s(), name='heartbeat every 10s')

@celery.task
def ping():
    r.set('beat_check', 'alive')
