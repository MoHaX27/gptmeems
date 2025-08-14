"""Async wrapper around ccxt.bybit for fetching market data."""
from __future__ import annotations

import asyncio
from typing import List

import ccxt.async_support as ccxt

from config.config import BYBIT_API_KEY, BYBIT_API_SECRET


class BybitClient:
    """Lightweight asynchronous CCXT Bybit client."""

    def __init__(self) -> None:
        self.client = ccxt.bybit({
            "apiKey": BYBIT_API_KEY,
            "secret": BYBIT_API_SECRET,
            "enableRateLimit": True,
        })

    async def fetch_ohlcv(self, symbol: str, timeframe: str = "1h", limit: int = 200):
        """Fetch OHLCV data for a single symbol."""
        return await self.client.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)

    async def fetch_many(self, symbols: List[str], timeframe: str = "1h", limit: int = 200):
        """Fetch OHLCV data for multiple symbols concurrently."""
        tasks = [self.fetch_ohlcv(s, timeframe=timeframe, limit=limit) for s in symbols]
        return await asyncio.gather(*tasks)

    async def close(self) -> None:
        await self.client.close()


async def main():
    client = BybitClient()
    try:
        print(await client.fetch_ohlcv("BTC/USDT", "1h", 5))
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
