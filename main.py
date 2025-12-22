import asyncio 
from bot.client import DiscordBot
import os
from dotenv import load_dotenv
from services.keep_alive import keep_alive

load_dotenv()

def main():
    bot = DiscordBot()
    bot.run(os.getenv("token"))

if __name__ == "__main__":
    main()