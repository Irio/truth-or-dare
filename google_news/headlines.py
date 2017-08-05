import feedparser
from google.cloud import datastore
import pandas as pd


class Headlines:
    """
    Handle ingestion of headlines from Google News' frontpage.
    """

    URL = 'https://news.google.com/news/rss/headlines?ned=pt-BR_br&hl=pt-BR'
    DATASTORE_KIND = 'google_news_article'

    def __init__(self, datastore_client=None):
        self.datastore_client = datastore_client or datastore.Client()

    @classmethod
    def entry_dict(cls, feed_entry):
        """
        Return a dict representation of a feed entry, with less fields.
        """
        return {
            'id': feed_entry['id'],
            'link': feed_entry['link'],
            'published': pd.to_datetime(feed_entry['published']),
            'title': feed_entry['title'],
        }

    def feed(self):
        """
        Return a list of 20 articles, in form of dictionaries,
        currently listed in the frontpage.
        """
        feed_dict = feedparser.parse(self.URL)
        return [self.entry_dict(entry) for entry in feed_dict['entries']]

    def store(self):
        """
        Store the feed headlines in the provided datastore.
        """
        articles = []
        for entry in self.feed():
            key = self.datastore_client.key(self.DATASTORE_KIND, entry['id'])
            article = datastore.Entity(key=key)
            article.update(entry)
            articles.append(article)
        self.datastore_client.put_multi(articles)
