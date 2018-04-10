import pdb
from enum import Enum

import tweepy

from tweet_analyse import settings


class Places(Enum):
    INDIA = 23424848
    WORLDWIDE = 1


class TweePy:
    def __init__(self, user):
        auth = tweepy.OAuthHandler(settings.SOCIAL_AUTH_TWITTER_KEY, settings.SOCIAL_AUTH_TWITTER_SECRET)

        auth.set_access_token(user.social_auth.get().extra_data['access_token']['oauth_token'],
                              user.social_auth.get().extra_data['access_token']['oauth_token_secret'])
        self.api = tweepy.API(auth)

    def get_trends(self):
        return self.api.trends_place(Places.INDIA.value)

    def search(self, q, since_id=None, max_id=None):
        return self.api.search(lang='en', q=q, count=100, result_type='recent', since_id=since_id, max_id=max_id)
