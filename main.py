import discord

import Controller.SystemController as SC

from discord.ext import commands

import config

TOKEN = config.access_token

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())


@bot.command()
async def start(ctx):
    sc = SC.SystemController(ctx)
    # TODO

bot.run(TOKEN)
