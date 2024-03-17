from my_commands.stock_index import index_info
from my_commands.stock_price import stock_price
from my_commands.stock_news import stock_search
from my_commands.stock_value import stock_value
from my_commands.analysis import stock_analysis

from discord import app_commands
from discord.ext import commands

import discord
import ApiKey


token = ApiKey.DISCORD_BOT_TOKEN

intents = discord.Intents.default()  # 取得預設的 intent
intents.message_content = True  # 啟用訊息內容

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
    embed = discord.Embed(title="大盤指數資訊/漲跌家數", description=index_block)
    await interaction.response.send_message(embed=embed)


# 個股資訊按鈕類別
class StockButtons(discord.ui.View):
    def __init__(self, stock_id):
        super().__init__(timeout=None)
        self.stock_index = stock_id

    # StockGPT 按鈕
    @discord.ui.button(label="StockGPT", style=discord.ButtonStyle.primary)
    async def stock_gpt(
        self, interaction: discord.Interaction, Button: discord.ui.Button
    ):
        # 因為後端程式的執行時間較長, 使用 defer 方法來延遲回應
        await interaction.response.defer()
        # 機器人正在思考
        async with interaction.channel.typing():
            gpt_reply = stock_analysis(self.stock_index)
        await interaction.followup.send(gpt_reply)

    # 股價按鈕
    @discord.ui.button(label="股價", style=discord.ButtonStyle.primary)
    async def stock_price(
        self, interaction: discord.Interaction, Button: discord.ui.Button
    ):
        await interaction.response.defer()
        stock_data = stock_price(self.stock_index)
        stock_block = "```\n" + stock_data + "```"
        title = f"{self.stock_index} 各日成交資訊"
        # 建立內嵌訊息
        embed = discord.Embed(title=title, description=stock_block)
        await interaction.followup.send(embed=embed)

    # 日殖利率、本益比及淨值比按鈕
    @discord.ui.button(label="日殖利率、本益比及淨值比", style=discord.ButtonStyle.primary)
    async def stock_value(
        self, interaction: discord.Interaction, Button: discord.ui.Button
    ):
        await interaction.response.defer()
        stock_data = stock_value(self.stock_index)
        stock_block = "```\n" + stock_data + "```"
        title = f"{self.stock_index} 個股日殖利率、本益比及股價淨值比"
        # 建立內嵌訊息
        embed = discord.Embed(title=title, description=stock_block)
        await interaction.followup.send(embed=embed)

    # 新聞資訊按鈕
    @discord.ui.button(label="新聞資訊", style=discord.ButtonStyle.primary)
    async def stock_news(
        self, interaction: discord.Interaction, Button: discord.ui.Button
    ):
        await interaction.response.defer()
        news_data = stock_search(self.stock_index)
        await interaction.followup.send(news_data)


# 斜線指令呼叫按鈕選單
@client.tree.command(name="stock_info", description="搜尋個股資訊")
@app_commands.rename(stock_id="股票代碼")
@app_commands.describe(stock_id="輸入要查詢的股票代碼, 如：2330")
async def stock_info(interaction: discord.Interaction, stock_id: str):
    content = f"股票代碼：{stock_id}, 請點擊想要查詢的資訊類型"
    await interaction.response.send_message(
        content=content, view=StockButtons(stock_id)
    )


client.run(token)
