import json

class PortoflioImage:
    def __init__(self, id, name, starting, buying_power, balance, adj, portfolio, stale):
        self.id = id
        self.name = name
        self.starting = starting
        self.buying_power = buying_power
        self.balance = balance
        self.adj = adj
        self.portfolio = json.dumps(portfolio)
        self.stale = stale
    def toObj(self):
       return { 
        "id": self.id,
        "name": self.name,
        "starting": self.starting, 
        "buying_power": self.buying_power, 
        "balance": self.balance, 
        "adj": self.adj, 
        "portoflio": self.portfolio, 
        "stale": self.stale  
        }

class TransactionImage:
    def __init__(self, id, type, symbol, amount, price):
        self.id = id
        self.type = type
        self.symbol = symbol
        self.amount = amount
        self.price = price
    def toObj(self):
       return { 
        "id": self.id,
        "type": self.type,
        "symbol": self.symbol, 
        "amount": self.amount, 
        "price": self.price,
        }