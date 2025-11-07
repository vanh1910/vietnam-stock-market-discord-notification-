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
    @commands.hybrid_group(
            name="stock", 
            description="for stock gamblers"
    )
    async def stock(self, context: Context, *args) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Please specify a subcommand"
            )
        await context.send(embed=embed)
    
    @stock.command(
        name = "price",
        description = "get latest price"
    )
    async def price(self, context:Context, ticker):
        data = self.stock_api.fetch_realtime_data("1D", pd.Timedelta(15,"d"), ticker)
        if len(data["c"]) == 0:
            message = f"Currently no {ticker} price"
        else:
            price = data["c"][-1]
            message = f"{ticker} price currently is {price}"
    
        await context.send(message)


    


async def setup(bot) -> None:
    await bot.add_cog(Stock(bot))

def test():
    api = APIHandler()
    range = pd.Timedelta(15,"d")
    data = api.fetch_realtime_data("1D", range, "VCB")
    return data["c"][-1]
        
if __name__ == "__main__":
    print(test())

