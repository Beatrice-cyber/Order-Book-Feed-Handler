# models.py
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass(frozen=True)
class Level:
    price: Decimal
    quantity: Decimal

@dataclass
class OrderBook:
    exchange: str
    symbol: str
    bids: list[Level]      # highest price first
    asks: list[Level]      # lowest price first
    timestamp: datetime
