import aiohttp
import discord
import random
import asyncio
import pandas as pd
from discord import app_commands
from discord.ext import commands, tasks
from discord.ext.commands import Context
from services.api_handler import StockAPIHandler

class Stock(commands.Cog, name="stock"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.stock_api = StockAPIHandler()
        self.update_ticker.start()
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
                f"Failed to insert {ticker} into tickers_users {exception}"
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
    
    @tasks.loop(seconds=60)
    async def update_ticker(self) -> None:
        #get tickers from db watchlist
        tickers = await self.bot.database.get_all_tickers()
        to_date = pd.Timestamp.now() - pd.Timedelta(hours=10)
        from_date = to_date - pd.Timedelta(minutes = 1)
        results = []
        #fetch data from vietstock
        try:
            results = await self.stock_api.get_historical_tickers_data(tickers, from_date, to_date, "1")
        except Exception as e:
            exception = f"{type(e).__name__}: {e}"
            self.bot.logger.error(
                f"Failed to fetch data: {exception}"
            )
        
        #push fetched data to db

        db_tasks = []
        for result in results:
            if (result["s"] == "no_data"): continue
            db_tasks.append(asyncio.create_task(self.bot.database.add_ticker_row(
                result["params"]["symbol"],
                result["t"][-1],
                result["params"]["resolution"],
                result["h"][-1],
                result["l"][-1],
                result["o"][-1],
                result["c"][-1],
                result["v"][-1],
            )))

        await asyncio.gather(*db_tasks)


    @update_ticker.before_loop
    async def before_update_ticker(self) -> None:
        self.bot.logger.info(
            "Realtime updating is ready"
        )
        await self.bot.wait_until_ready()






async def setup(bot) -> None:
    await bot.add_cog(Stock(bot))

def test():
    api = StockAPIHandler()
    range = pd.Timedelta(15,"d")
    data = api.fetch_realtime_data("1D", range, "VCB")
    return data["c"][-1]

        
if __name__ == "__main__":
    test()

