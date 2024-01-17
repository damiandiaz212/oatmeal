import requests

class Alpha:
    def __init__(self, key):
        self.key = key
    def quote(self, symbol):
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={self.key}'
        r = requests.get(url)
        data = r.json()
        if "Global Quote" in data:
            return data["Global Quote"]
        else:
            return False
    def price(self, symbol):
        resp = self.quote(symbol)
        if resp == False:
            return False
        return resp["05. price"]