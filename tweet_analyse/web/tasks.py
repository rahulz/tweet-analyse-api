from __future__ import absolute_import, unicode_literals

import base64
import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User

from tweet_analyse.celery import app
from utils.wordcloud import wordcloud
from utils.ai.sentiment import analyse_tweets
from utils.tweepy.helpers import TweePy


@app.task()
def generate_report(query, channel_name, user_pk):
    c = get_channel_layer()
    send = async_to_sync(c.send)
    user = User.objects.get(pk=user_pk)
    send(channel_name, {'type': 'update_client', 'data': {'progress': 1, 'label': 'Getting tweets'}})
    tp = TweePy(user)
    tweets = tp.search(query)
    if not tweets:
        send(channel_name,
             {'type': 'update_client', 'data': {'progress': -2, 'label': 'No tweets found, try with another keyword'}})
        return None

    send(channel_name, {'type': 'update_client',
                        'data': {'progress': 20, 'label': 'Generating sentiment analysis graph',
                                 'tweets_count': len(tweets)}})
    sentiment = analyse_tweets(tweets)
    send(channel_name, {'type': 'update_client',
                        'data': {'progress': 40, 'label': 'Generating wordcloud'}})

    img = wordcloud(' '.join([tweet.text for tweet in tweets]), fmt='png', query=query)
    data = {'progress': 100,
            'label': 'Done',
            'result': {
                'sentiment': sentiment,
                'wordcloud': "data:image/png;base64," + base64.b64encode(img.read()).decode("utf-8")}}
    send(channel_name, {'type': 'update_client',
                        'data': data})
    return query
