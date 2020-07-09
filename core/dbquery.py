import aiohttp
from aiohttp import ClientResponse


async def _validate_response(response) -> bool:
    if response.status == 200:
        return True
    else:
        async with open("error_log", "a") as f:
            f.write(response)
        return False


async def _produce_rtn_string(r: ClientResponse, source_anime: bool = False) -> str:
    if await _validate_response(r):
        r_json = await r.json()
        if not r_json:
            return "No quotes found."
        else:
            string = f"{r_json[0]['quote']} - {r_json[0]['character']}"
            return f"{string}, {r_json[0]['anime']}" if source_anime else string
    return "There was an error while retrieving quote."


async def get_random_quote(client: aiohttp.ClientSession) -> str:
    async with client.get("https://anime-chan.herokuapp.com/api/quotes/random") as r:
        output = await _produce_rtn_string(r, True)
        return output


async def get_character_quote(client: aiohttp.ClientSession, character: str) -> str:
    if not character:
        return "Character must be specified."
    async with client.get(f"https://anime-chan.herokuapp.com/api/quotes?char={character.lower()}") as r:
        output = await _produce_rtn_string(r)
        return output


async def get_anime_quote(client: aiohttp.ClientSession, anime: str) -> str:
    if not anime:
        return "Anime must be specified."
    async with client.get(f"https://anime-chan.herokuapp.com/api/quotes?anime={anime.lower()}") as r:
        output = await _produce_rtn_string(r)
        return output
