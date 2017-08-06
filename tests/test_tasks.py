from unittest import TestCase
from unittest.mock import patch

import tasks


class TestTasks(TestCase):
    @patch('tasks.Headlines')
    def test_collect_google_news(self, headlines_mock):
        tasks.collect_google_news()
        headlines_mock.return_value.store.assert_called_once()
