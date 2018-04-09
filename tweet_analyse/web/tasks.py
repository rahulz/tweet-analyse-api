from __future__ import absolute_import, unicode_literals

from time import sleep

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from tweet_analyse.celery import app


@app.task()
def generate_report(query, channel):
    c = get_channel_layer()
    print(channel)
    async_to_sync(c.send)(channel, {'type': 'update_client', 'data': {'status': 10}})
    sleep(10)
    async_to_sync(c.send)(channel, {'type': 'update_client', 'data': {'status': 20}})
    sleep(10)
    async_to_sync(c.send)(channel, {'type': 'update_client', 'data': {'status': 30}})
    sleep(10)
    async_to_sync(c.send)(channel, {'type': 'update_client', 'data': {'status': 30}})
