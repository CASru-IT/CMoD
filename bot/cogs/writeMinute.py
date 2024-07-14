from discord import app_commands
from discord.ext import commands
import discord
import os

guild_ids = int(os.getenv("GUILDS"))
class writeMinute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="minute")
    @discord.app_commands.guilds(guild_ids)
    async def writeMinute_command(self, interaction: discord.Interaction):
        """議事録を書く."""
        if interaction.user.voice is None:
            await interaction.response.send_message("あなたはボイスチャンネルに接続していません。")
            return