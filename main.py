import asyncio 
from bot.client import DiscordBot
import os
from dotenv import load_dotenv
# from services.api_handler import api_handler
from services.keep_alive import keep_alive

keep_alive()

# def test_api_handler():
#     resolution = "10"
#     range = pd.Timedelta(2, "d")
#     ticker = "VIC"
#     handler = api_handler()
#     handler.fetch_realtime_data(resolution, range, ticker)

load_dotenv()



def main():
    bot = DiscordBot()
    bot.run(os.getenv("token"))

if __name__ == "__main__":
    # test_api_handler()
    main()