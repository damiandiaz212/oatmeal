import requests

class Alpha:
    def __init__(self, key):
        self.key = key
    def fetch(self, url):
        r = requests.get(url)
        try:
            data = r.json()
            return data
        except:
            return {}
    def quote(self, symbol):
        resp = self.fetch(f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&entitlement=delayed&apikey={self.key}')
        if "Information" in resp:
            return False
        quote = next(iter(resp))
        return resp[quote]
    def price(self, symbol):
        resp = self.quote(symbol.upper())
        if resp == False: 
            return {"error" : 'Unable to execute order, no action was taken. Alpha service api limit may have been reached.' }
        if "05. price" not in resp:
            return {"error" : f'Unable to execute order, no action was taken. Empy object returned, check SYMBOL: {symbol}' }
        return { "value" : float(resp["05. price"]) }
    def sentiment(self):
        resp = self.fetch(f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={self.key}')
        if "feed" not in resp:
            return {"error" : f'Unable to fetch sentiment; response may have been empty.' }
        return resp["feed"][0]