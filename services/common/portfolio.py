from common.util import format_sse
from common.types import PortoflioImage

class MockPortfolio:
    def __init__(self, id, name, balance, alpha, announcer):
        self.id = id
        self.name = name
        self.starting = balance
        self.buying_power = balance
        self.alpha_svc = alpha
        self.announcer = announcer
        self.portfolio = dict()
    def ex_buy(self, symbol, amount):
        price = self.alpha_svc.price(symbol)
        if type(price) is not float and "error" in price:
            return price
        if symbol in self.portfolio:
            return { "error": f"Already owns {symbol} in portfolio." }
        self.portfolio[symbol] = { "price": price, "amount": amount }
        self.buying_power -= (price * amount)
        order =  { "order": "buy", "symbol": symbol, "amount": amount, "price": price  }
        msg = format_sse(data=order)
        self.announcer.announce(msg=msg)
        return {}, 200
    def ex_sell_all(self, symbol):
        price = self.alpha_svc.price(symbol)
        if type(price) is not float and "error" in price:
            return price
        if not symbol in self.portfolio:
            return { "error": f"Does not own {symbol} in portfolio." }
        order = self.portfolio.pop(symbol)
        self.buying_power += ( price * order["amount"] )
        adjusted = (price * order["amount"]) - (order["price"] * order["amount"])
        order = { "order": "sell", "symbol": symbol, "amount": order["amount"], "price": price, "gain/loss": adjusted  }
        msg = format_sse(data=order)
        self.announcer.announce(msg=msg)
        return {}, 200
    def status(self):
        standing = self.buying_power
        stale = False
        for key, value in self.portfolio.items():
            price = self.alpha_svc.price(key)
            if not price:
                stale = True
                standing += (value["price"] * value["amount"])
                print("Unable to fetch updated values, using stale data.")
            else:
                standing += (price * value["amount"])
        adjusted = (standing - self.starting)
        return PortoflioImage(self.id, self.name, self.starting, self.buying_power, standing, adjusted, self.portfolio, stale)