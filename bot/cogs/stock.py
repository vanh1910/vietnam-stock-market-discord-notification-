import aiohttp
import discord
import pandas as pd
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from services.api_handler import APIHandler

class Stock(commands.Cog, name="stock"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.stock_api = APIHandler()
    """
        Main stock command handler

        Usage:
            n4!stock save tickers (price)
            n4!stock remove tickers
            n4!stock price
            
            n4!chart tickers (this one will be done last) webhook?


        """
    @commands.command(name="stockprice", description="get lastest stock price of a ticker")
    async def stock(self, context: Context, ticker) -> None:
        data = self.stock_api.fetch_realtime_data("1H", pd.Timedelta(3,"d"), ticker)
        await context.send(data)


async def setup(bot) -> None:
    await bot.add_cog(Stock(bot))
        


