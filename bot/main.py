import discord
from discord.ext import commands
import os

from cogs.drawOmikuji import drawOmikuji
from cogs.writeMinute import writeMinute
from cogs.calendar import Calendar
from cogs.member import Member

BOT_COMMANDS = [drawOmikuji,  Calendar, writeMinute, Member]

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
    Calendar.my_loop.start()


@bot.event
async def on_message(message):
    name=message.author.global_name
    discordid=message.author.id
    username=message.author.name
    await bot.process_commands(message)
    await Member.on_message(message,name,discordid,username,bot)
    print(f"{message.channel}:{message.author}:{message.content}")
bot.run(DISCORD_BOT_TOKEN)
