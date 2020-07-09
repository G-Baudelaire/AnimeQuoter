import asyncio
import unittest

import aiohttp

from core.dbquery import get_random_quote, get_character_quote


class TestDBQueryMethods(unittest.TestCase):
    @classmethod
    async def _open_client(cls):
        return aiohttp.ClientSession()

    @classmethod
    async def _close_client(cls):
        await cls._client.close()

    @classmethod
    def setUpClass(cls) -> None:
        print("S")
        cls._loop = asyncio.get_event_loop()
        cls._client = cls._loop.run_until_complete(cls._open_client())

    @classmethod
    def tearDownClass(cls) -> None:
        print("T")
        cls._loop.run_until_complete(cls._client.close())
        cls._loop.close()

    def test_get_random_quote(self):
        output = self._loop.run_until_complete(get_random_quote(self._client))
        self.assertNotIn(output, ("There was an error while retrieving quote.", "No quotes found."))

    def test_get_character_quote_blank(self):
        output = self._loop.run_until_complete(get_character_quote(self._client, ""))
        self.assertEqual("Character must be specified.", output)

    def test_get_character_quote_charater(self):
        output = self._loop.run_until_complete(get_character_quote(self._client, "Sora"))
        self.assertNotEqual("Character not specified.", output)
