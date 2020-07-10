import asyncio
import unittest

import aiohttp

from core.dbquery import get_random_quote, get_character_quote, get_anime_quote


class CustomTestCase(unittest.TestCase):
    @classmethod
    async def _open_client(cls):
        return aiohttp.ClientSession()

    @classmethod
    async def _close_client(cls):
        await cls._client.close()

    @classmethod
    def setUpClass(cls) -> None:
        cls._loop = asyncio.new_event_loop()
        cls._client = cls._loop.run_until_complete(cls._open_client())

    @classmethod
    def tearDownClass(cls) -> None:
        cls._loop.run_until_complete(cls._client.close())
        cls._loop.close()


class TestDBQueryGetRandomQuoteMethod(CustomTestCase):
    def test_get_random_quote(self):
        output = self._loop.run_until_complete(get_random_quote(self._client))
        self.assertNotIn(output, ("There was an error while retrieving quote.", "No quotes found."))


class TestDBQueryGetCharacterQuoteMethod(CustomTestCase):
    def test_blank_character(self):
        output = self._loop.run_until_complete(get_character_quote(self._client, ""))
        self.assertEqual("Character must be specified.", output)

    def test_non_existent_character(self):
        output = self._loop.run_until_complete(get_character_quote(self._client, "akldjflkadklaf;ldkadsgdasggs"))
        self.assertEqual("No quotes found.", output)

    def test_url_character(self):
        output = self._loop.run_until_complete(get_character_quote(self._client, "https://github.com/"))
        self.assertEqual("No quotes found.", output)

    def test_real_character(self):
        output = self._loop.run_until_complete(get_character_quote(self._client, "Sora"))
        self.assertNotIn(output, ("Character must be specified.", "No quotes found."))


class TestDBQueryGetAnimeQuoteMethod(CustomTestCase):
    def test_blank_anime(self):
        output = self._loop.run_until_complete(get_anime_quote(self._client, ""))
        self.assertEqual("Anime must be specified.", output)

    def test_non_existent_anime(self):
        output = self._loop.run_until_complete(get_anime_quote(self._client, "akldjflkadklafldkadsgdasggs"))
        self.assertEqual("No quotes found.", output)

    def test_url_anime(self):
        output = self._loop.run_until_complete(get_anime_quote(self._client, "https://github.com/"))
        self.assertEqual("No quotes found.", output)

    def test_valid_anime(self):
        output = self._loop.run_until_complete(get_anime_quote(self._client, "Fairy Tail"))
        self.assertNotIn(output, ("Anime must be specified.", "No quotes found."))
