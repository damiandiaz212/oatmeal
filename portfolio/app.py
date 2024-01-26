from flask import Flask, send_from_directory, send_file, render_template
from flask_cors import cross_origin, CORS
from flask import request, jsonify, make_response, Response
from common.alpha import Alpha
from common.portfolio import MockPortfolio
from common.util import getAlphaKey, format_sse
from common.messager import MessageAnnouncer
from common.types import PortoflioImage
from service.persistence import Database
import os
import sys
import json
import uuid

app = Flask(__name__, static_url_path='', static_folder='dist', template_folder='dist')
CORS(app)

isLocal = len(sys.argv) > 1 and sys.argv[1] == '--local'
key = getAlphaKey(isLocal)
alpha = Alpha(key)
db = Database('portfolio.db')

portfolios = dict()

def setup():
   db.create_table()
   images = db.load_all().fetchall()
   for image in images:
      temp_announcer = MessageAnnouncer()
      temp_portfolio = PortoflioImage(image[0], image[1], image[2], image[3], image[4], image[5], '', True)
      portfolio_obj = json.loads(image[6])
      p_temp = MockPortfolio(-1, -1, -1, alpha, temp_announcer)
      p_temp.id = temp_portfolio.id;
      p_temp.name = temp_portfolio.name;
      p_temp.starting = temp_portfolio.starting;
      p_temp.buying_power = temp_portfolio.buying_power;
      p_temp.balance = temp_portfolio.balance;
      p_temp.adj = temp_portfolio.adj;
      p_temp.portfolio = portfolio_obj
      portfolios[temp_portfolio.id] = p_temp

def validate(request):
   id = request.args.get('id')
   if not id:
      return { "status" : 400, "message": "param 'id' is required" }
   return { "status": 200, "id": id }

@app.route("/")
@cross_origin()
def hello():
    return render_template("index.html")

@app.route('/api/stream')
@cross_origin()
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
   response = Response(stream(validation["id"]), mimetype='text/event-stream')
   response.headers.add("Access-Control-Allow-Origin", "*")
   return response

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
      db.save(portfolios[validation["id"]].status())
      return {}, 200
   return order

@app.route('/api/sell_all/<symbol>')
def sell_all(symbol):
   validation = validate(request)
   if validation["status"] != 200:
      return validation["message"], validation["status"]
   order = portfolios[validation["id"]].ex_sell_all(symbol)
   if "error" not in order:
      db.save(portfolios[validation["id"]].status())
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
