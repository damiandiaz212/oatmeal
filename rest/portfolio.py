class Portfolio:
    def __init__(self, balance, alpha):
        self.starting = balance
        self.buying_power = balance
        self.alpha_svc = alpha
        self.portfolio = dict()
    def ex_buy(self, symbol, amount):
        price = self.alpha_svc.price(symbol)
        if not price:
            return { "error": "Unable to execute order, no action was taken. Alpha service api limit may have been reached." }
        self.portfolio[symbol] = { "price": price, "amount": amount }
        self.buying_power -= (price * amount)
        return { "order": "buy", "symbol": symbol, "amount": amount, "price": price  }
    def ex_sell_all(self, symbol):
        price = self.alpha_svc.price(symbol)
        if not price:
            return { "error": "Unable to execute order, no action was taken. Alpha service api limit may have been reached." }
        order = self.portfolio.pop(symbol)
        self.buying_power += ( price * order["amount"] )
        adjusted = (price * order["amount"]) - (order["price"] * order["price"])
        return { "order": "sell", "symbol": symbol, "amount": amount, "price": price, "gain/loss": adjusted  }
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
        return { "starting": self.starting, "buying_power": self.buying_power, "balance": standing, "gain/loss": adjusted, "portoflio": self.portfolio, "stale": stale  }