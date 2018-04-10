import re

import pandas
from textblob import TextBlob


def clean_tweet(text):
    """
    Utility function to clean the text in a tweet by removing
    links and special characters using regex.
    """
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())


def analyse_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    return analysis.sentiment


def analyse_tweets(tweets):
    sentiment = []
    for tweet in tweets:
        analysis = TextBlob(clean_tweet(tweet.text))
        sentiment.append(analysis.sentiment)
    df = pandas.DataFrame(sentiment)
    try:
        ret = {'positive_sum': df[df['polarity'] > 0].sum(numeric_only=True).polarity / df.count()[0] * 100,
               'negative_sum': df[df['polarity'] < 0].sum(numeric_only=True).polarity / df.count()[0] * 100,
               'counts': [
                   int(df[df['polarity'] > 0].count()[0]),
                   int(df[df['polarity'] < 0].count()[0]),
                   int(df[df['polarity'] == 0].count()[0]),
               ]
               }
    except KeyError:
        return {'positive_sum': 0,
                'negative_sum': 0,
                'counts': [0, 0, 0]
                }
    print(ret)
    return ret
