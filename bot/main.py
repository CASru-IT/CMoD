import discord
from discord.ext import commands
import os
from discord.ext import tasks
from cogs.drawOmikuji import drawOmikuji
from cogs.writeMinute import writeMinute
from cogs.calendar import Calendar
from cogs.member import Member
from datetime import timedelta,timezone,time
BOT_COMMANDS = [drawOmikuji,  Calendar, writeMinute, Member]

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILDS = os.getenv("GUILDS")
JST = timezone(timedelta(hours=+9), "JST")
times = [
    time(hour=10, tzinfo=JST),
    time(hour=23, minute=35, tzinfo=JST)
]
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user}として接続しました。")
    for command in BOT_COMMANDS:
        await bot.add_cog(command(bot))
    await bot.tree.sync(guild=discord.Object(id=GUILDS))
    my_loop.start()


@tasks.loop(time=times)
async def my_loop():
    await Calendar.my_loop()

@bot.event
async def on_message(message):
    name=message.author.global_name
    discordid=message.author.id
    username=message.author.name
    await bot.process_commands(message)
    await Member.on_message(message,name,discordid,username,bot)
    print(f"{message.channel}:{message.author}:{message.content}")
bot.run(DISCORD_BOT_TOKEN)
