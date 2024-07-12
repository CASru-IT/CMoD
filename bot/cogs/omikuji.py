import random
from discord import app_commands
from discord.ext import commands
import discord
import os

guild_ids = int(os.getenv("GUILDS"))
class omikujicommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="omikuji")
    @discord.app_commands.guilds(guild_ids)
    async def omikuji_command(self, interaction: discord.Interaction):
        """おみくじを引く."""
        choice = random.choice(['大吉', '吉', '小吉', '凶', '大凶'])
        await interaction.response.send_message(f"あなたの今日の運勢は **{choice}** です!")