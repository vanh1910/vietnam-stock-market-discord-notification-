

import aiohttp
import asyncio
import json
import pandas as pd
import logging
from typing import Optional, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AsyncAPIHandler:
    BASE_URL = "https://api.vietstock.vn/tvnew/history"
    HEADERS = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Origin": "https://stockchart.vietstock.vn",
        "Referer": "https://stockchart.vietstock.vn/"
    }

    def __init__(self, timeout: int = 5):
        self.timeout = aiohttp.ClientTimeout(total=timeout)

    async def fetch_history(
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

    async def fetch_realtime_data(
        self,
        session: aiohttp.ClientSession,
        resolution: str,
        range_: pd.Timedelta,
        ticker: str
    ) -> Optional[Dict[str, Any]]:
        """Lấy dữ liệu thời gian thực (dạng async)."""
        to_date = pd.Timestamp.now()
        from_date = to_date - range_
        return await self.fetch_history(session, from_date, to_date, ticker, resolution)


async def main():
    handler = AsyncAPIHandler()
    range_ = pd.Timedelta(days=2)
    tickers = ["VND", "FPT", "SSI", "HPG", "VCB"]

    async with aiohttp.ClientSession(timeout=handler.timeout) as session:
        tasks = [
            handler.fetch_realtime_data(session, "1", range_, ticker)
            for ticker in tickers
        ]
        results = await asyncio.gather(*tasks)

    # Lưu tất cả kết quả ra file
    with open("data/json/realtime_cache.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    logger.info("Đã tải xong tất cả dữ liệu song song.")


if __name__ == "__main__":
    asyncio.run(main())
