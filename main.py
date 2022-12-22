import discord
import Controller.SystemController as SC
from discord.ext import commands

TOKEN = "MTAxNDkxMTc4OTA1OTgwOTMyMA.GW_uD1.IHZ6bDklLaUP6Fb9Brrcu4o_Zfd_QGRtSHXK-8"

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())


@bot.command()
async def start(ctx):
    sc = SC.SystemController(ctx)
    print("1.")
    print(sc.global_points)
    print("\n")

    sc.calculate_points()
    print("2.")
    print(sc.global_points)
    print("\n")

    input()
    sc.refresh_global_points()
    print("3.")
    print(sc.global_points)

    # TODO

bot.run(TOKEN)
