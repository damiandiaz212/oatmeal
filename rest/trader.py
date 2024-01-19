import time
from alpha import Alpha
from sentiment import SentimentTrader
import os

key = '9YMZNZBVZOUKAHOT'

alpha = Alpha(key)
trader = SentimentTrader(alpha, 1000)

starttime = time.time()

def heartbeat():
    print("heartbeat", flush=True)
    trader.examine_sentiment()

while True:
    heartbeat()
    time.sleep(5)
