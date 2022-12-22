import asyncio
import datetime

import discord
import Controller.SystemController as SC
from discord.ext import commands
import config

TOKEN = config.access_token

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())


@bot.command()
async def start(ctx):
    sc = SC.SystemController(ctx)
    await sc.start()


@bot.command()
async def clear(ctx):
    [await m.delete() async for m in ctx.channel.history(limit=500)]


@bot.command()
async def test(ctx):
    ts_in_ten_secs = int(datetime.datetime.now().timestamp()) + 10

    await ctx.send(content="<t:" + str(ts_in_ten_secs) + ":R>")


bot.run(TOKEN)
