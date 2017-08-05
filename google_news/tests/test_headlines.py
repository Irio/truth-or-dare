import itertools
import json
from unittest import TestCase
from unittest.mock import MagicMock

from google_news.headlines import Headlines as subject_class
import pandas as pd
import vcr


class TestStringMethods(TestCase):
    def setUp(self):
        self.datastore_client = MagicMock()
        self.subject = subject_class(datastore_client=self.datastore_client)

    def test_entry_dict(self):
        with open('google_news/fixtures/feed_entry.json') as json_file:
            feed_entry = json.load(json_file)
            expected = {
                'id': 'tag:news.google.com,2005:cluster=d1k_TwdXEsMJgCMkDjaj0f7wanMZM',
                'link': 'http://g1.globo.com/economia/noticia/com-ingresso-de-r-233-bilhoes-poupanca-tem-melhor-saldo-para-julho-em-3-anos.ghtml',
                'published': pd.Timestamp('2017-08-04 18:33:00'),
                'title': 'Com ingresso de R$ 2,33 bilhões, poupança tem melhor julho em 3 anos',
            }
            self.assertEqual(expected, subject_class.entry_dict(feed_entry))

    @vcr.use_cassette('google_news/fixtures/vcr_cassettes/headlines_feed.yaml')
    def test_feed(self):
        self.assertEqual(20, len(self.subject.feed()))

    @vcr.use_cassette('google_news/fixtures/vcr_cassettes/headlines_store.yaml')
    def test_store(self):
        self.subject.store()
        articles_properties = self.datastore_client.put_multi.call_args_list[0][0][0]
        returned = [call.items() for call in articles_properties]
        expected = [entry.items() for entry in self.subject.feed()]
        self.assertEqual(expected, returned)
