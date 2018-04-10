from io import BytesIO

from wordcloud import WordCloud, STOPWORDS

for s in ['retweets', 'retweet', 'direct message', 'likes', 'RT', 'http', 'https', 'co', 'com']:
    STOPWORDS.add(s)


def wordcloud(data, title=None, fmt='plt', query=""):
    STOPWORDS.add(query)
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt
    plt.figure(figsize=(15, 8))
    plt.axis('off')
    # if title:
    #     fig.suptitle(title, fontsize=20)
    #     fig.subplots_adjust(top=2.3)

    plt.imshow(WordCloud(
        background_color="rgba(255, 255, 255, 0)", mode="RGBA",
        width=800,
        height=400,
        stopwords=STOPWORDS,
        scale=4
    ).generate(str(data)), interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    if fmt == 'plt':
        return plt
    else:
        img = BytesIO()
        plt.savefig(img, bbox_inches='tight', format=fmt, transparent=True)
        img.seek(0)
        return img
