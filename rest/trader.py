import time
from alpha import Alpha
from sentiment import SentimentTrader
import os

key = os.environ["API_KEY"]

alpha = Alpha(key)
trader = SentimentTrader(alpha, 1000)

starttime = time.time()

def heartbeat():
    print("heartbeat")
    trader.examine_sentiment()

while True:
    heartbeat()
    time.sleep(5)
