import discord
import ApiKey
import re

token = ApiKey.DISCORD_BOT_TOKEN

intents = discord.Intents.default()     # 取得預設的 intent
intents.message_content = True          # 啟用訊息內容

client = discord.Client(intents=intents)

# 標記使用者時在訊息中的格式為 <@username>
pattern_mention = re.compile(r'\s{0,1}<@\d+>\s')


@client.event
async def on_ready():
    print(f'{client.user} is login!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # 只處理 @機器人 的訊息
    if client.user in message.mentions:
        msg = re.sub(pattern_mention, '', message.content)          # 移除訊息中指名的資訊
        await message.channel.send(f'{message.author.mention} {msg}')   # 回覆時指名原發言者


client.run(token)
