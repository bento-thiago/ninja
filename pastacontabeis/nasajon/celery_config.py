from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nasajon.settings')

user_rabbitmq = os.getenv('rabbitmq_user', 'rabbit_user')
password_rabbitmq = os.getenv('rabbitmq_password', 'my_secret_password')
host_rabbitmq = os.getenv('rabbitmq_host', 'localhost')
port_rabbitmq = os.getenv('rabbitmq_port', '5672')
vhost_rabbitmq = os.getenv('rabbitmq_vhost', '')

celery_broker_url = 'pyamqp://{user}:{password}@{host}:{port}/{vhost}'.format(
    user=user_rabbitmq,
    password=password_rabbitmq,
    host=host_rabbitmq,
    port=port_rabbitmq,
    vhost=vhost_rabbitmq
)

app = Celery('nasajon', broker=celery_broker_url)
# app = Celery('nasajon')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='celery')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# TODO Apagar depois:
# Testando o enfileiramento de mensagens
# from nasajon.pastas_contabeis.pastas_router import notificar, MomentoContabil
# notificar.delay("abstract_pasta_contabil.AbstractPastContabil", MomentoContabil.CANCELAMENTO.value, dict())
