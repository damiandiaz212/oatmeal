from common.util import format_sse
from common.types import PortoflioImage

class MockPortfolio:
    def __init__(self, id, name, balance, alpha):
        self.id = id
        self.name = name
        self.starting = balance
        self.buying_power = balance
        self.alpha_svc = alpha
        self.portfolio = dict()
    def ex_buy(self, symbol, amount):
        price = self.alpha_svc.price(symbol)
        if "error" in price:
            return price, 500
        if price["value"] * amount > self.buying_power:
            return {"error": "order declined. not enough funds"}, 200
        if symbol in self.portfolio:
            return { "error": f"Already owns {symbol} in portfolio." }, 200
        self.portfolio[symbol] = { "price": price["value"], "amount": amount }
        self.buying_power -= (price["value"] * amount)
        order =  { "order": "buy", "symbol": symbol, "amount": amount, "price": price["value"]  }
        return order, 200
    def ex_sell_all(self, symbol):
        price = self.alpha_svc.price(symbol)
        if "error" in price:
            return price, 500
        if not symbol in self.portfolio:
            return { "error": f"Does not own {symbol} in portfolio." }, 200
        order = self.portfolio.pop(symbol)
        self.buying_power += ( price["value"] * order["amount"] )
        adjusted = round((price["value"] * order["amount"]) - (order["price"] * order["amount"]), 2)
        order = { "order": "sell", "symbol": symbol, "amount": order["amount"], "price": price["value"], "gain/loss": adjusted  }
        return order, 200
    def status(self):
        standing = self.buying_power
        stale = False
        for key, value in self.portfolio.items():
            price = self.alpha_svc.price(key)
            if "error" in price:
                stale = True
                standing += (value["price"] * value["amount"])
                print("Unable to fetch updated values, using stale data.")
            else:
                standing += (price["value"] * value["amount"])
        adjusted = (standing - self.starting)
        return PortoflioImage(self.id, self.name, round(self.starting, 2), round(self.buying_power, 2), round(standing, 2), round(adjusted, 2), self.portfolio, stale)