import discord
import random
import json
import asyncio
from discord.ext import commands
import os

BOT_COMMANDS = []
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

class MyClient(commands.Bot):
    def __init__(self, command_prefix="/", *args, **kwargs):
        super().__init__(command_prefix="/", *args, **kwargs)

    async def on_ready(self):
        print(f"{self.user}として接続しました。")

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        print(f"{message.author}よりメッセージを受信しました: {message.content}")
        await super().on_message(message)

intents = discord.Intents.all()
client = MyClient(intents=intents)
for command in BOT_COMMANDS:
    client.add_command(command)
client.run(DISCORD_BOT_TOKEN)
