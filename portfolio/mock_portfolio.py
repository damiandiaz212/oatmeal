from flask import Flask, send_from_directory, send_file
from flask_cors import cross_origin, CORS
from flask import request, jsonify, make_response, Response
from common.alpha import Alpha
from common.portfolio import MockPortfolio
from common.util import getAlphaKey, format_sse
from common.messager import MessageAnnouncer
from service.persistence import Database
import os
import sys
import json
import uuid

app = Flask(__name__)
CORS(app)

isLocal = len(sys.argv) > 1 and sys.argv[1] == '--local'
key = getAlphaKey(isLocal)
alpha = Alpha(key)
db = Database('portfolio.db')

portfolios = dict()

def setup():
   images = db.load_all()
   for image in images:
      temp = MessageAnnouncer()
      p_temp = MockPortfolio(image[0], image[1], image[2], alpha, temp)
      p_temp.starting = image[3]
      p_temp.buying_power = image[4]
      p_temp.portfolio = json.loads(image[6])
      portfolios[p_temp.id] = p_temp
   print('Loaded in memory', portfolios)

@app.route('/api/<id>/stream')
def feed(id):
   def stream(id):
      messages = portfolios[id].announcer.listen()
      while True:
         message = messages.get()
         yield message
   return Response(stream(id), mimetype='text/event-stream')

@app.route('/api/<id>/status')
def status(id):
   return portfolios[id].status().toObj()

@app.route('/api/<id>/reset/<balance>')
def reset(id, balance):
   name = portfolios[id].name
   announcer = portfolios[id].announcer
   portfolios[id] = MockPortfolio(id, name, balance, alpha, announcer)
   return {}, 200

@app.route('/api/<id>/buy/<symbol>/<amount>')
def buy(id, symbol, amount):
   order = portfolios[id].ex_buy(symbol, int(amount))
   if "error" not in order:
      return {}, 200
   return order

@app.route('/api/<id>/sell_all/<symbol>')
def sell_all(id, symbol):
   order = portfolios[id].ex_sell_all(symbol)
   if "error" not in order:
      return {}, 200
   return order

@app.route('/api/create/<name>/<balance>')
def create(name, balance):
   id = str(uuid.uuid4())
   temp = MessageAnnouncer()
   portfolios[id] = MockPortfolio(id, name, float(balance), alpha, temp)
   return portfolios[id].status().toObj(), 200

@app.route('/api/save')
def save():
   for p in portfolios.values():
      db.save(p.status())
   return {}, 200

if (__name__ == "__main__"):
   setup()
   app.run(debug=True)