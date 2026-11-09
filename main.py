import asyncio

import binance
import storage
from analytics import depth, spread

async def main():
    conn = storage.connect()

    def handle(book):
        s = spread(book)
        bd, ad = depth(book.bids), depth(book.asks)
        print(f"{book.symbol} spread={s} bid_depth={bd} ask_depth={ad}")
        storage.save(conn, book, s, bd, ad)

    await binance.stream(handle)

if __name__ == "__main__":
    asyncio.run(main())