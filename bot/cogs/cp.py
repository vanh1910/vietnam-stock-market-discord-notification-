from discord.ext import commands,tasks
from discord.ext.commands import Context
import discord
import aiohttp
import asyncio
import random
import datetime
from services.api_handler import CPAPIHandler
import os

owner_id = os.getenv('OWNER_ID')

# Here we name the cog and create a new class for the cog.

class SubmitButton(discord.ui.View):
    def __init__(self, handle, platform, problem) -> None:
        super().__init__(timeout=None)
        self.handle = handle
        self.platform = platform
        self.problem = problem
        self.cp_api = CPAPIHandler()
        self.result = False

    @discord.ui.button(label="Done", style=discord.ButtonStyle.blurple)
    async def submit_button_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
        ):
        # Acknowledge the interaction immediately
        await interaction.response.defer()
        
        try:
            subs = await self.cp_api.fetch_user_submission(self.handle)
            for sub in subs["result"]:
                problem_id = f"{sub['problem']['contestId']}{sub['problem']['index']}"
                expected_id = f"{self.problem['contestId']}{self.problem['index']}"
                
                if problem_id == expected_id and sub["verdict"] == "COMPILATION_ERROR":
                    self.result = True
                    self.stop()
                    return
            
            self.stop()
            #await interaction.followup.send("❌ No compilation error found on this problem. Please try again.")
        except Exception as e:
            await interaction.followup.send(f"❌ Error checking submissions: {str(e)}")
            
        self.stop()

        

        

        




class CP(commands.Cog, name="cp"):
    daily_problem_time = datetime.time(hour=0, tzinfo=datetime.timezone.utc)

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
    async def set(self, context:Context) -> None:
        """
            Add server channel, or dm for daily problems
        """
        channel_id = context.channel.id
        if context.guild:
            if not (context.message.author.guild_permissions.administrator or context.message.author.id == int(owner_id)):
                return
                
        await self.bot.database.add_cp_channel_row(channel_id)
        await context.reply("Registering channel completely")

    @cp.command(
        name = "unset",
        description = "unset channel for daily cp problems"
    )
    async def unset(self, context:Context) -> None:
        """
            Add server channel, or dm for daily problems
        """
        channel_id = context.channel.id
        if context.guild:
            if not (context.message.author.guild_permissions.administrator or context.message.author.id == int(owner_id)):
                return
                
        await self.bot.database.remove_cp_channel_row(channel_id)
        await context.reply("Unset channel completely")



    @cp.command(
        name = "save",
        description = "Save your cp accounts (*Currently only support cf*)"
    )
    async def save(self, context: Context, platform, handle):
        problem = await self.cp_api.true_random_problem()
        problem_link = f"https://codeforces.com/contest/{problem['contestId']}/problem/{problem['index']}"
        user_id = context.author.id

        button = SubmitButton(handle, platform, problem)
        embed = discord.Embed(
            color = 0xCCCCCC,
            description=f"Please submit a compilation error to [this problem]({problem_link})\n"
                        "When you are done, press the button below",
        )
        message = await context.send(embed=embed, view=button)
        await asyncio.sleep(0.1) 
        
        try:
            # Set a timeout of 300 seconds (5 minutes)
            await asyncio.wait_for(button.wait(), timeout=300)
        except asyncio.TimeoutError:
            embed = discord.Embed(
                description="⏰ Verification timed out. Please try again.",
                color=0xFF0000
            )
            await message.edit(embed=embed, view=None)
            return
        
        print(button.result)

        if button.result:
            await self.bot.database.add_cp_acc_row(user_id,handle,platform)
            embed = discord.Embed(
                description="✅ You are now signed in uwu!!",
                color=0x00FF00
            )
            await message.edit(embed=embed, view=None)
        else:
            embed = discord.Embed(
                description=f"❌ Please resubmit the [problem]({problem_link}) :3",
                color=0xFF0000
            )
            await message.edit(embed=embed, view=button)

        

        

    @cp.command(
        name = "random",
        description= "get random cp problem"
    )
    async def random_problem(self, context:Context):
        """
            Replying random problem to user message
        """
        problem = await self.cp_api.random_problem()
        problem_link = f"https://codeforces.com/contest/{problem['contestId']}/problem/{problem['index']}"
        embed = discord.Embed(
            title=f"{problem['contestId']}{problem['index']} - {problem['name']}",
            url=problem_link, # Click vào tiêu đề sẽ mở link
            color=self.__get_rating_color(problem.get('rating', 0)) # Set màu theo rating
        )
        embed.add_field(name="📊 Rating", value=f"`{problem.get('rating', 'Unrated')}`", inline=True)
        embed.set_thumbnail(url="https://sta.codeforces.com/s/70808/images/codeforces-telegram-square.png")

        await context.reply(embed=embed)



    @cp.command(
        name = "truerandom",
        description = "Random problem without weight"
    )
    async def true_random_problem(self, context: Context):
        """
            Replying true random problem to user message
        """
        problem = await self.cp_api.true_random_problem()
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
            problem = await self.cp_api.random_problem()
            if problem != None: 
                break
        

               

async def setup(bot) -> None:
    await bot.add_cog(CP(bot))