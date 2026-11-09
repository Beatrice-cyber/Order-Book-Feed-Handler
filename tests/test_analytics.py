# tests/test_analytics.py
from datetime import datetime, timezone
from decimal import Decimal

from analytics import depth, spread
from models import Level, OrderBook


def make_book(bids, asks):
    """Build an OrderBook from lists of (price, quantity) pairs."""
    return OrderBook(
        exchange="test",
        symbol="BTCUSDT",
        bids=[Level(Decimal(p), Decimal(q)) for p, q in bids],
        asks=[Level(Decimal(p), Decimal(q)) for p, q in asks],
        timestamp=datetime.now(timezone.utc),
    )


def test_spread_normal():
    book = make_book(bids=[("67000", "1")], asks=[("67010", "1")])
    assert spread(book) == Decimal("10")


def test_spread_no_bids():
    book = make_book(bids=[], asks=[("67010", "1")])
    assert spread(book) is None


def test_spread_no_asks():
    book = make_book(bids=[("67000", "1")], asks=[])
    assert spread(book) is None


def test_spread_empty_book():
    assert spread(make_book(bids=[], asks=[])) is None


def test_depth_sums_top_n_only():
    book = make_book(
        bids=[("100", "1"), ("99", "2"), ("98", "3"), ("97", "4")],
        asks=[],
    )
    assert depth(book.bids, n=2) == Decimal("3")   # 1 + 2, ignores the rest


def test_depth_fewer_levels_than_n():
    book = make_book(bids=[("100", "1"), ("99", "2")], asks=[])
    assert depth(book.bids, n=5) == Decimal("3")   # no crash when n is too big


def test_depth_empty_side():
    assert depth([], n=5) == 0