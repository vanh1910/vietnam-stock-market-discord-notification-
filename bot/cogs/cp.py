from discord.ext import commands,tasks
from discord.ext.commands import Context
import discord
import aiohttp
import asyncio
import random
import datetime
from services.api_handler import CPAPIHandler

# Here we name the cog and create a new class for the cog.

class CP(commands.Cog, name="cp"):
    daily_problem_time = datetime.time(hour=2, tzinfo=datetime.timezone.utc)

    def __init__(self, bot) -> None:
        self.bot = bot
        self.cp_api = CPAPIHandler()

    def __get_rating_color(self, rating):
        if rating < 1200: return 0xCCCCCC # Gray (Newbie)
        if rating < 1400: return 0x77FF77 # Green (Pupil)
        if rating < 1600: return 0x03A89E # Cyan (Specialist)
        if rating < 1900: return 0x0000FF # Blue (Expert)
        if rating < 2100: return 0xAA00AA # Violet (Candidate Master)
        if rating < 2300: return 0xFF8C00 # Orange (Master)
        if rating < 2400: return 0xFF8C00 # Orange (International Master) - CF dùng chung màu cam
        if rating < 2600: return 0xFF0000 # Red (Grandmaster)
        return 0xFF0000 # Red (Legendary GM)
        
    @commands.hybrid_group(
            name="cp", 
            description="commands for cp grinders"
    )
    async def cp(self, context: Context, *args) -> None:
        """
            Init function for cp cog
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Please specify a subcommand"
            )
        await context.reply(embed=embed)



    @cp.command(
        name = "set",
        description = "set channel for daily cp problems, or register dm for daily cp problems"
    )
    async def set(self, context:Context):
        """
            Add server channel, or dm for daily problems
        """
        pass




    @cp.command(
        name = "random",
        description= "get random cp problem"
    )
    async def random_problem(self, context:Context):
        problem = {}
        low = 800
        high = 3500
        for i in range (10):
            problem = await self.cp_api.fetch_random_problem(low,high)
            if problem != None: 
                break
        
        problem_link = f"https://codeforces.com/contest/{problem['contestId']}/problem/{problem['index']}"
        embed = discord.Embed(
            title=f"{problem['contestId']}{problem['index']} - {problem['name']}",
            url=problem_link, # Click vào tiêu đề sẽ mở link
            description=f"**Type:** {problem['type'].title()}",
            color=self.__get_rating_color(problem.get('rating', 0)) # Set màu theo rating
        )
        embed.add_field(name="📊 Rating", value=f"`{problem.get('rating', 'Unrated')}`", inline=True)
        embed.set_thumbnail(url="https://sta.codeforces.com/s/70808/images/codeforces-telegram-square.png")

        await context.reply(embed=embed)
    

    @tasks.loop(time=daily_problem_time)
    async def daily_problem(self) -> None:
        problem = {}
        for i in range (10):
            problem = await self.cp_api.fetch_random_problem(800, 2300)
            if problem != None: 
                break
        

               

async def setup(bot) -> None:
    await bot.add_cog(CP(bot))