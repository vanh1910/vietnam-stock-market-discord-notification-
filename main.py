import pandas as pd

from services.api_handler import api_handler

def test_api_handler():
    resolution = "10"
    range = pd.Timedelta(2, "d")
    ticker = "VIC"
    handler = api_handler()
    handler.fetch_realtime_data(resolution, range, ticker)

if __name__ == "__main__":
    test_api_handler()