import discord
import ApiKey


token = ApiKey.DISCORD_BOT_TOKEN

intents = discord.Intents.default()     # 取得預設的 intent
intents.message_content = True          # 啟用訊息內容
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} is login!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await message.channel.send(message.content)


client.run(token)
