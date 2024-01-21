import time
from common.alpha import Alpha
from model.sentiment import SentimentTrader
from common.util import getVariable
import os

key = getVariable(True)

alpha = Alpha(key)
trader = SentimentTrader(alpha, 'http:/localhost:5000' ,1000)

starttime = time.time()

def heartbeat():
    print("heartbeat", flush=True)
    trader.examine_sentiment()

while True:
    heartbeat()
    time.sleep(5)
