import asyncio, json, websockets

URL = "wss://stream.binance.com:9443/ws/btcusdt@depth5"

import json
import websockets
from datetime import datetime, timezone
from decimal import Decimal
from models import Level, OrderBook

URL = "wss://stream.binance.com:9443/ws/btcusdt@depth5"

def parse(message: str, symbol: str = "BTCUSDT") -> OrderBook:
    data = json.loads(message)
    return OrderBook(
        exchange="binance",
        symbol=symbol,
        bids=[Level(Decimal(p), Decimal(q)) for p, q in data["bids"]],
        asks=[Level(Decimal(p), Decimal(q)) for p, q in data["asks"]],
        timestamp=datetime.now(timezone.utc),
    )

async def stream(on_book):
    delay = 1
    while True:
        try:
            async with websockets.connect(URL) as ws:
                delay = 1                      # connected, so reset the wait
                async for message in ws:
                    on_book(parse(message))
        except (websockets.ConnectionClosed, OSError) as e:
            print(f"Disconnected ({e}); retrying in {delay}s")
        await asyncio.sleep(delay)
        delay = min(delay * 2, 30)             # 1, 2, 4, 8 ... capped at 30s