import aiohttp
import discord
import asyncio
import pandas as pd
from discord import app_commands
from discord.ext import commands, tasks
from discord.ext.commands import Context
from services.api_handler import APIHandler

class Stock(commands.Cog, name="stock"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.stock_api = APIHandler()
    """
        Main stock command handler

        Usage:
            n4!stock add ticker
            n4!stock remove ticker
            n4!stock price
            n4!stock tickers

        """
    @commands.hybrid_group(
            name="stock", 
            description="for stock gamblers"
    )
    async def stock(self, context: Context, *args) -> None:
        """
            Get lastest price using vietstock API
        """
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
        async with aiohttp.ClientSession(timeout=self.stock_api.timeout) as session:
            data = await self.stock_api.fetch_realtime_data(
                session, "1D",
                pd.Timedelta(days=15),
                ticker
                )
        try:
            price = data['c'][-1]
            await context.reply(f"{ticker} price currently is {price}")
        except:
            await context.reply(f"Cannot get {ticker} price")
            


    @stock.command(
        name="add",
        description="register ticker into watchlist"
    )
    async def add_ticker(self, context:Context, ticker):
        """
            Add ticker into your watchlist
        """
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
        """
            Remove ticker from your watchlist
        """
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
        """
            Get all currently tickers in database
        """
        tickers = await self.bot.database.get_all_tickers()
        await context.reply(tickers)    
    
    @tasks.loop(minutes=60)
    async def update_ticker(self) -> None:
        tickers = await self.bot.database.get_all_tickers()
        tasks = []
        for ticker in tickers:
            task = asyncio.create_task(self.stock_api.get_latest_tickers_data(ticker,1,"1"))
        
        




async def setup(bot) -> None:
    await bot.add_cog(Stock(bot))

def test():
    api = APIHandler()
    range = pd.Timedelta(15,"d")
    data = api.fetch_realtime_data("1D", range, "VCB")
    return data["c"][-1]

        
if __name__ == "__main__":
    test()

