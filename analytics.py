from decimal import Decimal
# spread(), depth(), mid_price()
# It should calculate how much money you would receive by selling a given BTC quantity 
# against the available bids, without placing a real trade.
def simulate_market_sell(bids, quantity):
    # [usdt, quantity]
    money= 0
    restq = quantity
    for p, q in bids:
        traded = min(restq, q)

        money += p * traded
        restq -= traded

        if restq == 0:
            break
    return money, restq

def execute_market_sell(bids, quantity):
    # Execute against bids
    # Update the remaining quantities
    # Remove fully consumed price levels
    # Return total proceeds and remaining quantity
    newbids =[]
    restq = quantity
    for p,q in bids:
        if restq >= q:
            restq -= q
        else:
            newbids.append([p,q-restq])
            restq =0
        if restq ==0:
            newbids.append([p,q])
    return newbids,restq

# spread = ask - bid 
def spread(book):
    if not book.bids or not book.asks:
        return None
    return book.asks[0].price - book.bids[0].price

def depth(levels, n=5):
    return sum((level.quantity for level in levels[:n]), Decimal("0"))
