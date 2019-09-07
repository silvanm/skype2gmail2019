import unittest
from datetime import datetime, date

from lib.importlib import MessagePreprocessor


def create_timestamp(datetime: datetime) -> float:
    return datetime.timestamp() * 1000


class TestImport(unittest.TestCase):

    def test_preprocess_messages(self):
        raw_messages = [
            {
                'from': '8:silvanm75',
                'version': create_timestamp(datetime(year=2019, month=9, day=7, hour=11, minute=12)),
                'content': 'I am the second line',
                'originalarrivaltime': '2017-04-21T07:47:15.014Z',
            },
            {
                'from': '8:silvanm75',
                'version': create_timestamp(datetime(year=2019, month=9, day=7, hour=11, minute=10)),
                'content': 'I am the first line',
                'originalarrivaltime': '2017-04-21T07:47:13.014Z',
            },
            {
                'from': '8:richard.lauper',
                'version': create_timestamp(datetime(year=2019, month=9, day=7, hour=11, minute=15)),
                'content': 'I am the response',
                'originalarrivaltime': '2017-04-21T07:47:16.014Z',
            },
            {
                'from': '8:richard.lauper',
                'version': create_timestamp(datetime(year=2019, month=9, day=8, hour=11, minute=15)),
                'content': 'This is another day',
                'originalarrivaltime': '2017-04-21T07:47:17.014Z',
            }
        ]
        p = MessagePreprocessor()
        self.assertEqual(p.preprocess_messages(raw_messages), [{'authors': {'silvanm75', 'richard.lauper'},
                                                                'date': date(2019, 9, 7),
                                                                'messages': [{'color': 180.0,
                                                                              'content': 'I am the first line<br>I am the second line',
                                                                              'date': date(2019, 9, 7),
                                                                              'datetime': datetime(2019, 9, 7,
                                                                                                            11, 10),
                                                                              'from': 'silvanm75'},
                                                                             {'color': 0.0,
                                                                              'content': 'I am the response',
                                                                              'date': date(2019, 9, 7),
                                                                              'datetime': datetime(2019, 9, 7,
                                                                                                            11, 15),
                                                                              'from': 'richard.lauper'}]},
                                                               {'authors': {'richard.lauper'},
                                                                'date': date(2019, 9, 8),
                                                                'messages': [{'color': 0.0,
                                                                              'content': 'This is another day',
                                                                              'date': date(2019, 9, 8),
                                                                              'datetime': datetime(2019, 9, 8,
                                                                                                            11, 15),
                                                                              'from': 'richard.lauper'}]}])

    def test_preprocess_messages_empty(self):
        raw_messages = [
        ]
        p = MessagePreprocessor()
        self.assertEqual(p.preprocess_messages(raw_messages), [])

    def test_preprocess_messages_ignore_before(self):
        raw_messages = [
            {
                'from': '8:silvanm75',
                'version': create_timestamp(datetime(year=2018, month=9, day=7, hour=11, minute=12)),
                'content': 'I am the second line',
                'originalarrivaltime': '2017-04-21T07:47:15.014Z',
            },
            {
                'from': '8:silvanm75',
                'version': create_timestamp(datetime(year=2019, month=9, day=7, hour=11, minute=10)),
                'content': 'I am the first line',
                'originalarrivaltime': '2017-04-21T07:47:13.014Z',
            }
        ]
        p = MessagePreprocessor()
        self.assertEqual(len(p.preprocess_messages(raw_messages, ignore_before=datetime(year=2019, month=1, day=1))), 1)


if __name__ == '__main__':
    unittest.main()
