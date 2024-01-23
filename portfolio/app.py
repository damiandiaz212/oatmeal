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
   images = db.load_all().fetchall()
   for image in images:
      temp = MessageAnnouncer()
      p_temp = MockPortfolio(image[0], image[1], image[2], alpha, temp)
      p_temp.starting = image[3]
      p_temp.buying_power = image[4]
      p_temp.portfolio = json.loads(image[6])
      portfolios[p_temp.id] = p_temp

def validate(request):
   id = request.args.get('id')
   if not id:
      return { "status" : 400, "message": "param 'id' is required" }
   return { "status": 200, "id": id }

@app.route('/api/stream')
def feed():
   def stream(id):
      try:
         messages = portfolios[id].announcer.listen()
         while True:
            message = messages.get()
            yield message
      except:
         return f"id:{id} does not exist in portfolio", 404
   validation = validate(request)
   if validation["status"] != 200:
      return validation["message"], validation["status"]
   return Response(stream(validation["id"]), mimetype='text/event-stream')

@app.route('/api/ids')
def ids():
   return list(portfolios.keys())

@app.route('/api/status')
def status():
   validation = validate(request)
   if validation["status"] != 200:
      return validation["message"], validation["status"]
   return portfolios[validation["id"]].status().toObj()

@app.route('/api/delete')
def delete():
   validation = validate(request)
   if validation["status"] != 200:
      return validation["message"], validation["status"]
   return db.delete(validation["id"])

@app.route('/api/reset/<balance>')
def reset(balance):
   validation = validate(request)
   if validation["status"] != 200:
      return validation["message"], validation["status"]
   name = portfolios[validation["id"]].name
   announcer = portfolios[validation["id"]].announcer
   portfolios[validation["id"]] = MockPortfolio(id, name, balance, alpha, announcer)
   return {}, 200

@app.route('/api/buy/<symbol>/<amount>')
def buy(symbol, amount):
   validation = validate(request)
   if validation["status"] != 200:
      return validation["message"], validation["status"]
   order = portfolios[validation["id"]].ex_buy(symbol, int(amount))
   if "error" not in order:
      return {}, 200
   return order

@app.route('/api/sell_all/<symbol>')
def sell_all(symbol):
   validation = validate(request)
   if validation["status"] != 200:
      return validation["message"], validation["status"]
   order = portfolios[validation["id"]].ex_sell_all(symbol)
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
   app.run()