class SentimentTrader:
    def __init__(self, alpha, max_order_cost):
        self.alpha = alpha
        self.max_order_cost = max_order_cost
    def is_bullish(self, entry):
        return entry['ticker_sentiment_label'] == 'Somewhat-Bullish' or entry['ticker_sentiment_label'] == 'Bullish'
    def is_bearish(self, entry):
        return entry['ticker_sentiment_label'] == 'Somewhat-Bearish' or entry['ticker_sentiment_label'] == 'Bearish'
    def examine_sentiment(self):
        orders = []
        sentiment = self.alpha.sentiment()
        if not sentiment:
            print('Api limit reached')
            return 
        tickers = sentiment['ticker_sentiment']
        for entry in tickers:
            symbol = entry['ticker']
            if len(symbol) > 4:
                continue
            elif self.is_bullish(entry) and symbol not in self.portfolio.portfolio:
                amt = int(abs(self.max_order_cost / self.alpha.price(symbol)))
                url = f'/api/buy/{symbol}/{amt}'
                r = requests.get(url)
                data = r.json()
                orders.append(data)
            elif self.is_bearish(entry) and symbol in self.portfolio.portfolio:
                url = f'/api/sell_all/{symbol}'
                r = requests.get(url)
                data = r.json()
                orders.append(data)
        print(orders)