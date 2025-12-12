import random
import aiohttp
import asyncio
import json
import pandas as pd
import logging
from typing import Optional, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StockAPIHandler:
    BASE_URL = "https://api.vietstock.vn/tvnew/history"
    HEADERS = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Origin": "https://stockchart.vietstock.vn",
        "Referer": "https://stockchart.vietstock.vn/"
    }

    def __init__(self, timeout: int = 5):
        self.timeout = aiohttp.ClientTimeout(total=timeout)

    async def __fetch_history(
        self,
        session: aiohttp.ClientSession,
        from_date: pd.Timestamp,
        to_date: pd.Timestamp,
        ticker: str,
        resolution: str
    ) -> Optional[Dict[str, Any]]:
        """Lấy dữ liệu lịch sử của cổ phiếu từ Vietstock API."""
        from_ts = int(from_date.timestamp())
        to_ts = int(to_date.timestamp())

        params = {
            "symbol": ticker,
            "resolution": resolution,
            "from": from_ts,
            "to": to_ts,
            "countback": 2
        }

        try:
            async with session.get(
                self.BASE_URL,
                headers=self.HEADERS,
                params=params
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
                data["params"] = params
                return data

        except aiohttp.ClientError as e:
            logger.error(f"API request failed for {ticker}: {e}")
            return None

    async def __fetch_realtime_data(
        self,
        session: aiohttp.ClientSession,
        resolution: str,
        range_: pd.Timedelta,
        ticker: str
    ) -> Optional[Dict[str, Any]]:
        """Lấy dữ liệu thời gian thực."""
        to_date = pd.Timestamp.now()
        from_date = to_date - range_
        return await self.__fetch_history(session, from_date, to_date, ticker, resolution)

    async def get_latest_tickers_data(self,tickers: list, from_date: pd.Timestamp, resolution: str):
        """
            Get price from a list of tickers from 'from_date' to now
            Args:
                tickers (list[str]): A list of ticker symbols
                from_date (pd.Timestam) Start time
                resolution (str): Time resolution, only accept "1", "60", "1D"
        """
        to_date = pd.Timestamp.now()
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            tasks = [
                self.__fetch_history(session, from_date, to_date, ticker, resolution)
                for ticker in tickers
            ]
            results = await asyncio.gather(*tasks)
        
        with open("data/json/realtime_cache.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        return results

    async def get_historical_tickers_data(
        self,
        tickers: list,
        from_date: pd.Timestamp,
        to_date: pd.Timestamp,
        resolution: str
    ):
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            tasks = [
                self.__fetch_history(session, from_date, to_date, ticker, resolution)
                for ticker in tickers
            ]
            results = await asyncio.gather(*tasks)
        with open("data/json/realtime_cache.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        return results

class CPAPIHandler:
    BASE_URL = " https://codeforces.com/api/"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json',
        'Connection': 'keep-alive'
    }
    def __init__(self, timeout: int = 20):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        

    async def fetch_problem(self):
        tags = ['*special', '2-sat', 'binary search', 'bitmasks', 'brute force', 'chinese remainder theorem', 'combinatorics', 'constructive algorithms', 'data structures', 'dfs and similar', 'divide and conquer', 'dp', 'dsu', 'expression parsing', 'fft', 'flows', 'games', 'geometry', 'graph matchings', 'graphs', 'greedy', 'hashing', 'implementation', 'interactive', 'math', 'matrices', 'meet-in-the-middle', 'number theory', 'probabilities', 'schedules', 'shortest paths', 'sortings', 'string suffix structures', 'strings', 'ternary search', 'trees', 'two pointers']
        tag = random.choice(tags)
        
        url = self.BASE_URL + "problemset.problems"
        params = {
            "tags": tag
        }
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(
                    url,
                    headers=self.HEADERS,
                    params=params
                ) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
                    return data

        except aiohttp.ClientError as e:
            logger.error(f"API request failed: {e}")
            return None
        
    async def random_problem(self):
        data = await self.fetch_problem()
        problems = data["result"]["problems"]
        weights = []
        for problem in problems:
            rating = problem.get('rating', 0)
            if rating == 0 or rating > 2500:
                weights.append(20)
            elif rating > 1600: 
                weights.append(2*1600 - rating * 1.1 - (rating-1700)//1.5)
            else:
                weights.append(rating)
        
        return random.choices(problems, weights=weights, k=1)[0]
    

    async def true_random_problem(self):
        data = await self.fetch_problem()
        return random.choice(data["result"]["problems"])



    async def fetch_user_submission(self, handle, from_sub = 1, count_sub = 10):
        url = self.BASE_URL + "user.status"
        params = {
            "handle": handle,
            "from" : from_sub,
            "count": count_sub,
        }
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
               async with session.get(
                    url,
                    headers=self.HEADERS,
                    params=params
                ) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
                    return data
               
        except aiohttp.ClientError as e:
            logger.error(f"API request failed: {e}")
            return None

 
async def main():
    pass

if __name__ == "__main__":
    asyncio.run(main())
