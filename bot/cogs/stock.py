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
    @commands.command(name="stock", description="get lastest stock price of a ticker")
    async def stock(self, context: Context, *args) -> None:
        subcommand = args[0]
        message = ""
        match subcommand:
            case "price":
                ticker = args[1]
                price = self.get_price(ticker)
                message = f"{ticker} current price is {price}"
        
        await context.send(message)


                
    def get_price(self, ticker):
        range = pd.Timedelta(15,"d")
        data = self.stock_api.fetch_realtime_data("1D", range, ticker)
        return data["c"][-1]


async def setup(bot) -> None:
    await bot.add_cog(Stock(bot))

def test():
    api = APIHandler()
    range = pd.Timedelta(15,"d")
    data = api.fetch_realtime_data("1D", range, "VCB")
    return data["c"][-1]
        
if __name__ == "__main__":
    print(test())

