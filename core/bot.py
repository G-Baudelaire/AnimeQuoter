import os

import aiohttp
from discord.ext.commands import Bot, errors
from dotenv import load_dotenv

from core import dbquery

client = aiohttp.ClientSession()

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot = Bot(command_prefix="!quote ")


@bot.command(name="rand", help="Responds with a quote from a random character from a random anime.")
async def random_quote(ctx):
    quote = await dbquery.get_random_quote(client)
    await ctx.send(quote)


@bot.command(name="char", help="Responds with a random quote from a random anime character.")
async def character_quote(ctx, *args: str):
    quote = await dbquery.get_character_quote(client, " ".join(args))
    await ctx.send(quote)


@bot.command(name="ani", help="Responds with a random quote from an anime.")
async def anime_quote(ctx, *args: str):
    quote = await dbquery.get_anime_quote(client, " ".join(args))
    await ctx.send(quote)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, errors.CommandNotFound):
        await ctx.send("Command does not exist.")


if __name__ == '__main__':
    bot.run(TOKEN)
