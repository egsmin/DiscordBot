import asyncio
import datetime

import discord
import Controller.SystemController as SC
from discord.ext import commands
import config

TOKEN = config.access_token

# Erzeugen des Bots
bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())


@bot.command()
async def start(ctx):
    """ Start-Befehl des Bots

    Diese Methode ermoeglicht den $start Befehl in Discord

    :param ctx: Kontext
    :return:
    """
    # Erstellung und Starten des SystemControllers u
    sc = SC.SystemController(ctx)
    await sc.start()


@bot.command()
async def clear(ctx):
    """ Hilfsfunktion, um bis zu 500 Nachrichten im Chat zu loeschen.

    Bei Eingabe des $clear Befehls, werden bis zu 500 geloescht.

    :param ctx: Kontext, in dem die Nachrichten gesendet wurde.
    :return:
    """
    [await m.delete() async for m in ctx.channel.history(limit=500)]

# Starte den Bot
bot.run(TOKEN)
