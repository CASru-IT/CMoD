import random
from discord import app_commands
from discord.ext import commands
import discord
import os
from datetime import datetime, timedelta,timezone,time
from discord.ext import tasks
import discord
from discord import app_commands
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle

guild_ids = int(os.getenv("GUILDS"))
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
#CREDENTIALS_FILE = r"bot\config\client_secret_324197984736-s3ro8seiphkb0cqe8l1hdchguc2ktqa3.apps.googleusercontent.com.json"
#calenid="d6d3d2cbe1b43fbd2e4793d04637c1d8586a4d62dd39e3c445173d8ee6c7abfc@group.calendar.google.com"
CREDENTIALS_FILE = os.getenv("CREDENTIALS_FILE")
calenid = os.getenv("CALENDAR_ID")

pickle_file = r'bot\config\token.pickle'

intents = discord.Intents.default()
intents.message_content = True
channel_id = 1259377733268668426

client = discord.Client(intents=intents)
tree= app_commands.CommandTree(client)
JST = timezone(timedelta(hours=+9), "JST")
times = [
    time(hour=10, tzinfo=JST),
    time(hour=23, minute=35, tzinfo=JST)
]

def set_embed():
    global embed
    embed = discord.Embed( # Embedを定義する
                          title="Googleカレンダー",# タイトル
                          color=0x00ff00, # フレーム色指定(今回は緑)
                          description="予定一覧", # Embedの説明文 必要に応じて
                          url="https://calendar.google.com/calendar/embed?src=d6d3d2cbe1b43fbd2e4793d04637c1d8586a4d62dd39e3c445173d8ee6c7abfc%40group.calendar.google.com&ctz=Asia%2FTokyo" # これを設定すると、タイトルが指定URLへのリンクになる
                          )

def get_calendar_service():
    creds = None
    # token.pickle ファイルが存在する場合は、既にユーザー認証情報を保存している
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            creds = pickle.load(token)
    # 認証情報が無い場合、または無効な場合はユーザーにログインを要求する
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES)
            except FileNotFoundError:
                print("FileNotFoundError")
                return True
            creds = flow.run_local_server(port=0)
        # 次回のために認証情報を保存する
        with open(pickle_file, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


# Google Calendar APIを使用してカレンダーのイベントを取得
def list_events():
    service = get_calendar_service()
    if service is True:
        return None
    events_result = service.events().list(calendarId=calenid, timeMin='2020-01-01T00:00:00Z', maxResults=10, singleEvents=False).execute()
    events = events_result.get('items', [])

    if not events:
        return 'No upcoming events found.'
    
    events_info = []  # イベント情報を格納するためのリストを初期化
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        events_info.append((start, event['summary']))  # イベント情報をリストに追加

    for event in events_info:
        embed.add_field(name=event[0], value=event[1], inline=False)
    return "ok"

def reminder():
    service = get_calendar_service()
    # 現在の日付と翌日の日付を取得
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z'はUTCを指定
    tomorrow = (datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z'

    # カレンダーから予定を取得
    events_result = service.events().list(calendarId=calenid, timeMin=now, timeMax=tomorrow,
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        embed.add_field(name=start, value=event['summary'], inline=False) 

current_datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
class Calendar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    
        
    
    global stop_thread
    stop_thread = False

    @tasks.loop(time=times)
    async def my_loop():
        print("カレンダーサービスを取得しています...")
        set_embed()
        if not stop_thread:
            
            reminder()
            await client.wait_until_ready()
            channel=client.get_channel(channel_id)
            await channel.send(embed=embed)
        
    @app_commands.command(name="calendar", description="Googleカレンダーの予定を表示します")
    @discord.app_commands.guilds(guild_ids)
    async def calendar(self,interaction: discord.Interaction):
        set_embed()
        isfile=list_events()
        if isfile is None:
            await interaction.response.send_message(f"CREDENTIALS_FILEが見つかりませんでした", ephemeral=True)
            return
        await interaction.response.send_message(f"Googleカレンダーの予定を表示します", embed=embed, ephemeral=True)
        
    @app_commands.command(name="istime", description="現在時刻を表示します")
    @discord.app_commands.guilds(guild_ids)
    async def istime(self,interaction: discord.Interaction):
        await interaction.response.send_message(f"現在時刻は{current_datetime}です", ephemeral=True)

    @app_commands.command(name="noti", description="notification on or off")
    @discord.app_commands.guilds(guild_ids)
    async def noti(self,interaction: discord.Interaction,mode:bool):
        global stop_thread
        if mode:
            stop_thread = False
            await interaction.response.send_message(f"通知をオンにします", ephemeral=True)
        else:
            stop_thread = True
            await interaction.response.send_message(f"通知をオフにします", ephemeral=True)

