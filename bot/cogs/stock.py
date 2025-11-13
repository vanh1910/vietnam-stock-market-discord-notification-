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
        await context.reply(embed=embed)
    
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
    
        await context.reply(message)

    @stock.command(
        name="add",
        description="register ticker into watchlist"
    )
    async def add_ticker(self, context:Context, ticker):
        server_id = None
        if context.guild:
            server_id = context.guild.id
            
        user_id = context.author.id
        try: 
            await self.bot.database.add_ticker_user(
                user_id, ticker, server_id
            )
            await context.reply(f"Put {ticker} into watchlist successfully")
        except Exception as e:
            exception = f"{type(e).__name__}: {e}"
            self.logger.error(
                f"Failed to insert {ticker} into tickers_users {Exception}"
            )
            await context.reply(f"Failed to add {ticker} to watchlist")
            
    @stock.command(
        name="remove",
        description="remove ticker from watchlist"
    ) 
    async def remove_ticker(self, context:Context, ticker):
        user_id = context.author.id
        try:
            await self.bot.database.remove_tickers_users(user_id,ticker)
            await context.reply(f"Successfully remove {ticker} from watchlist")
        except Exception as e:
            exception = f"{type(e).__name__}: {e}"
            self.logger.error(
                f"Failed to remove {ticker} from tickers_users {Exception}"
            )
            await context.reply(f"Failed to remove {ticker} from watchlist")
            
    @stock.command(
        name="tickers",
        description="return all available tickers"
    )
    async def get_all_tickers(self, context:Context):
        tickers = await self.bot.database.get_all_tickers()
        await context.reply(tickers)    
    


async def setup(bot) -> None:
    await bot.add_cog(Stock(bot))

def test():
    api = APIHandler()
    range = pd.Timedelta(15,"d")
    data = api.fetch_realtime_data("1D", range, "VCB")
    return data["c"][-1]

        
if __name__ == "__main__":
    test()

