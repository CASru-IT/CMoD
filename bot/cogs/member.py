import discord
from discord import app_commands
import json
import os
import random
from discord import app_commands
from discord.ext import commands
import discord
import os


intents = discord.Intents.default()
intents.message_content = True
guild_ids = int(os.getenv("GUILDS"))

datafile='data//data.json'
attributefile='config//attribute.json'

client = discord.Client(intents=intents)
tree= app_commands.CommandTree(client)

def listdata():
    with open(attributefile, 'r', encoding='utf-8') as f:
        data1 = json.load(f)
        listdata=[]
        for k in data1["must"]["visible"]:
            listdata.append(k)
        for i in data1["must"]["invisible"]:
            listdata.append(i)
        return listdata

def setdata(discord_name: str,datatype:str,info:str):
    print("書き込み")
    with open(datafile) as f:
        data = json.load(f)
        if discord_name not in data:
            data[discord_name] = {}
        data[discord_name][datatype] = info  # 引数名を変更して、正しい値を設定
    with open(datafile, 'w') as f:
        json.dump(data, f, indent=4)

# ファイルが存在しない場合は空の JSON ファイルを作成
if not os.path.exists(datafile):
    os.makedirs(os.path.dirname(datafile), exist_ok=True)  # ディレクトリがない場合は作成
    with open(datafile, 'w') as f:
        json.dump({}, f)  # 空の JSON オブジェクトをファイルに書き込む


class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="get", description="リストを取得します")
    @discord.app_commands.guilds(guild_ids)
    async def get(self,interaction: discord.Interaction,discord_name: str):
        embed = discord.Embed(title="人の情報",color=0x00ff00)
        with open(datafile) as f:
            data = json.load(f)
            if discord_name not in data:
                await interaction.response.send_message(discord_name+"の情報が見つかりません", ephemeral=True)
                return
            persondata=data[discord_name]
        for k, v in persondata.items():  # キー／値の組を列挙
            embed.add_field(name=k, value=v, inline=False)
        await interaction.response.send_message(discord_name+f"の情報を表示します", embed=embed, ephemeral=True)

    @app_commands.command(name="set", description="リストに追加します")
    @discord.app_commands.guilds(guild_ids)
    async def set(self,interaction: discord.Interaction,discord_name: str,datatype:str,info:str):
        setdata(discord_name,datatype,info)
        await interaction.response.send_message(discord_name + "の情報を追加しました", ephemeral=True)



    @app_commands.command(name="search", description="リストを検索します")
    @discord.app_commands.guilds(guild_ids)
    async def search(self,interaction: discord.Interaction,datatype: str):
        embed = discord.Embed(title=datatype+"についての情報はこちら",color=0x00ff00)
        i =0
        with open(datafile) as f:
            data = json.load(f)
            persondata=data.items()
            for k1, v1 in persondata:
                for k2, v2 in v1.items():
                    if k2==datatype:
                        i+=1
                        embed.add_field(name=k1, value=v2, inline=False)
        await interaction.response.send_message(str(i)+"件の情報が見つかりました", embed=embed, ephemeral=True)

    @app_commands.command(name="searchall", description="リストを検索します")
    @discord.app_commands.guilds(guild_ids)
    async def searchall(self,interaction: discord.Interaction,datatype: str,info:str):
        embed = discord.Embed(title="人の情報",color=0x00ff00)
        namelist=[]
        result=""
        with open(datafile) as f:
            data = json.load(f)
            persondata=data.items()
            for k1, v1 in persondata:
                for k2, v2 in v1.items():
                    if k2==datatype and v2==info:
                        namelist.append(k1)
        for name in namelist:
            result+=name+"\n"
        embed.add_field(name=info+"の"+datatype+"を持つ人", value=result, inline=False)

        await interaction.response.send_message(str(len(namelist)+1)+"件の情報が見つかりました", embed=embed, ephemeral=True)

    @app_commands.command(name="list", description="リスト一覧を表示します")
    @discord.app_commands.guilds(guild_ids)
    async def list(self,interaction: discord.Interaction):
        embed = discord.Embed(title="人の情報",color=0x00ff00)
        result=""
        with open(datafile) as f:
            data = json.load(f)
            persondata=data.keys()
            for name in persondata:
                result+=name+"\n"
        embed.add_field(name="リスト", value=result, inline=False)
        await interaction.response.send_message("リストを表示します", embed=embed, ephemeral=True)

    @client.event
    async def on_message(message):
        writable=True
        if message.guild:
            return
        if message.author == client.user:
            return
        if not writable:
            return
        name=message.author.global_name
        discordid=message.author.id
        username=message.author.name
        setdata(name,"discordid",discordid)
        setdata(name,"username",username)
        #await message.channel.send("こんにちは")
        with open(attributefile, 'r', encoding='utf-8') as f:
            data1 = listdata()
            for attri in data1:
                with open(datafile) as f:
                    data = json.load(f)
                    if attri not in data[name]:
                        await message.channel.send(attri)
                        await message.channel.send("を入力してください")
                        writable=False
                        msg = await client.wait_for('message')
                        if msg.author == client.user:
                            continue
                        setdata(name,attri,msg.content)
                        writable=True
                        break
        


#client.run('MTI1OTAxODU0OTkwNTg1NDQ5NA.G8ITua.LtrznVyunTCkgNuwu9bAwC4o6LHSUsmF8QBkHc')