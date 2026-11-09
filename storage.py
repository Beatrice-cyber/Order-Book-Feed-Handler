# storage.py  writes snapshots to SQLite or Postgres
import sqlite3

def connect(path="feed.db"):
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exchange TEXT, symbol TEXT, ts TEXT,
            spread TEXT, bid_depth TEXT, ask_depth TEXT
        )
    """)
    return conn

def save(conn, book, spread, bid_depth, ask_depth):
    conn.execute(
        "INSERT INTO snapshots (exchange, symbol, ts, spread, bid_depth, ask_depth) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (
            book.exchange, book.symbol, book.timestamp.isoformat(),
            None if spread is None else str(spread),   # spread can be None
            str(bid_depth), str(ask_depth),
        ),
    )
    conn.commit()