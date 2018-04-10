from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

from tweet_analyse import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tweet_analyse.settings')

app = Celery('tweet_analyse')

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()

