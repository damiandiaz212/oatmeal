from flask import Flask, send_from_directory, send_file
from flask_cors import cross_origin
from flask import request, jsonify, make_response
from alpha import Alpha
from portfolio import Portfolio
import os

app = Flask(__name__)

key = os.environ["API_KEY"]

alpha = Alpha(key)
portfolio = Portfolio(10000, alpha)

feed = []

@app.route('/api/buy/<symbol>/<amount>')
def buy(symbol, amount):
   order = portfolio.ex_buy(symbol, int(amount))
   if "error" not in order:
      feed.append(order)
   return order

@app.route('/api/sell_all/<symbol>')
def sell_all(symbol):
   order = portfolio.ex_sell_all(symbol)
   if "error" not in order:
      feed.append(order)
   return order

@app.route('/api/status')
def status():
   print(feed)
   return portfolio.status()