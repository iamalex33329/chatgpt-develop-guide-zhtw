from my_commands.stock_index import index_info
from my_commands.stock_price import stock_price
from my_commands.stock_value import stock_value

from discord import app_commands
from discord.ext import commands

import discord
import ApiKey


token = ApiKey.DISCORD_BOT_TOKEN

intents = discord.Intents.default()  # 取得預設的 intent
intents.message_content = True  # 啟用訊息內容

# 建立指令機器人
client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print(f"{client.user} 已登入")
    try:
        synced = await client.tree.sync()
        print(f"{len(synced)}")
    except Exception as e:
        print(e)


# 大盤資訊查詢
@client.tree.command(name="index_info", description="搜尋最新大盤資訊")
async def dc_index(interaction: discord.Interaction):
    index_data = index_info()
    index_block = "```\n" + index_data + "```"
    # 建立內嵌訊息
    embed = discord.Embed(title="大盤指數資訊", description=index_block)
    await interaction.response.send_message(embed=embed)


# 個股股價資料
@client.tree.command(name="stock_price", description="搜尋最近股價資料")
@app_commands.rename(stock_id="股票代碼")
@app_commands.describe(stock_id="輸入要查詢的股票代碼, 如：2330")
async def dc_stock(interaction: discord.Interaction, stock_id: str):
    stock_data = stock_price(stock_id)
    stock_block = "```\n" + stock_data + "```"
    title = f"{stock_id} 各日成交資訊"
    # 建立內嵌訊息
    embed = discord.Embed(title=title, description=stock_block)
    await interaction.response.send_message(embed=embed)


# 個股殖利率、本益比及淨值比資料
@client.tree.command(name="stock_value", description="搜尋本益比、淨值比")
@app_commands.rename(stock_id="股票代碼")
@app_commands.describe(stock_id="輸入要查詢的股票代碼, 如：2330")
async def dc_value(interaction: discord.Interaction, stock_id: str):
    stock_data = stock_value(stock_id)
    stock_block = "```\n" + stock_data + "```"
    title = f"{stock_id} 個股日殖利率、本益比及股價淨值比"
    # 建立內嵌訊息
    embed = discord.Embed(title=title, description=stock_block)
    await interaction.response.send_message(embed=embed)


client.run(token)
