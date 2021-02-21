import json
from unittest import TestCase
from unittest.mock import AsyncMock, Mock

from aiounittest import AsyncTestCase
from airly import Airly
from airly._private import _DictToObj

LATITUDE = 12
LONGITUDE = 21

class _DictToObjTestCase(TestCase):
    def test_init_with_iterable(self):
        data = { 'key1': 'value1', 'key2': 2 }
        sut = _DictToObj(data)
        self.assertEqual('value1', sut['key1'])
        self.assertEqual('value1', sut.key1)
        self.assertEqual(2, sut['key2'])
        self.assertEqual(2, sut.key2)

    def test_init_with_kwargs(self):
        sut = _DictToObj(key1='value1', key2=2)
        self.assertEqual('value1', sut['key1'])
        self.assertEqual('value1', sut.key1)
        self.assertEqual(2, sut['key2'])
        self.assertEqual(2, sut.key2)


class HeadersTestCase(AsyncTestCase):
    async def test_valid_headers(self):
        with open("data/measurements_typical.json") as file:
            data = json.load(file)
        headers = {"X-RateLimit-Limit-day": "1000", "X-RateLimit-Remaining-day": "993"}
        with Mock(
            get=AsyncMock(side_effect=data),
            headers=Mock(side_effect=headers),
            status=200,
            __enter__=Mock(),
            __exit__=Mock(),
        ) as mock_session:
            airly = Airly("abcdef", mock_session)
            measurements = airly.create_measurements_session_point(LATITUDE, LONGITUDE)
            await measurements.update()
            assert airly.requests_per_day == 1000
            assert airly.requests_remaining == 993

    async def test_invalid_headers(self):
        with open("data/measurements_typical.json") as file:
            data = json.load(file)
        headers = {}
        with Mock(
            get=AsyncMock(side_effect=data),
            headers=Mock(side_effect=headers),
            status=200,
            __enter__=Mock(),
            __exit__=Mock(),
        ) as mock_session:
            airly = Airly("abcdef", mock_session)
            measurements = airly.create_measurements_session_point(LATITUDE, LONGITUDE)
            await measurements.update()
            assert airly.requests_per_day == None
            assert airly.requests_remaining == None