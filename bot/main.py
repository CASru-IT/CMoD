import discord
from discord.ext import commands
import os

from bot.cogs.drawOmikuji import drawOmikuji
from bot.cogs.writeMinute import writeMinute

BOT_COMMANDS = [drawOmikuji, writeMinute]

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILDS = os.getenv("GUILDS")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user}として接続しました。")
    for command in BOT_COMMANDS:
        await bot.add_cog(command(bot))
    await bot.tree.sync(guild=discord.Object(id=GUILDS))


bot.run(DISCORD_BOT_TOKEN)
