from flask import Flask, send_from_directory, send_file, render_template
from flask_cors import cross_origin, CORS
from flask import request, jsonify, make_response, Response
from common.alpha import Alpha
from common.portfolio import MockPortfolio
from common.util import get_alpha_key, format_sse, get_db_creds
from common.messager import MessageAnnouncer
from common.types import PortoflioImage
from repository.portfolio import PortfolioDB
from repository.transaction import TransactionDB
import os
import sys
import json
import uuid
import datetime

app = Flask(__name__, static_url_path='', static_folder='web/dist', template_folder='web/dist')
CORS(app)

is_local = len(sys.argv) > 1 and sys.argv[1] == '--local'
key = get_alpha_key(is_local)
db_path = get_db_creds(is_local)
alpha = Alpha(key)

portfolioDB = PortfolioDB(db_path)
transactionDB = TransactionDB(db_path)

portfolios = dict()
transactions = dict()

def setup():
   images = portfolioDB.load_all()
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
   for pid in portfolios.keys():
      transactions[pid] = transactionDB.fetch_all_by_id(pid)

def validate(request):
   id = request.args.get('id')
   if not id:
      return { "status" : 400, "message": "param 'id' is required" }
   return { "status": 200, "id": id }

@app.route('/')
def serve():
   return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/init')
def init():
   setup()
   return {}, 200

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

# @app.route('/api/delete')
# def delete():
#    validation = validate(request)
#    if validation["status"] != 200:
#       return validation["message"], validation["status"]
#    return db.delete(validation["id"])

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
   resp = portfolios[validation["id"]].ex_buy(symbol, int(amount))
   if "error" in resp:
      return resp
   order = resp[0]
   receipt = ( validation["id"], order["order"], order["symbol"], order["amount"], order["price"], str(datetime.datetime.now().timestamp()) )
   portfolioDB.update_entry(portfolios[validation["id"]].status())
   transactions[validation["id"]].append(receipt)
   transactionDB.append_entry(receipt)
   return {}, 200


@app.route('/api/sell_all/<symbol>')
def sell_all(symbol):
   validation = validate(request)
   if validation["status"] != 200:
      return validation["message"], validation["status"]
   resp = portfolios[validation["id"]].ex_sell_all(symbol)
   if "error" in resp:
         return resp
   order = resp[0]
   receipt = ( validation["id"], order["order"], order["symbol"], order["amount"], order["price"], str(datetime.datetime.now().timestamp()) )
   portfolioDB.update_entry(portfolios[validation["id"]].status())
   transactions[validation["id"]].append(receipt)
   transactionDB.append_entry(receipt)
   return {}, 200

@app.route('/api/create/<name>/<balance>')
def create(name, balance):
   id = str(uuid.uuid4())
   temp = MessageAnnouncer()
   portfolios[id] = MockPortfolio(id, name, float(balance), alpha, temp)
   portfolioDB.create_entry(portfolios[id].status())
   transactions[id] = []
   return portfolios[id].status().toObj(), 200

@app.route('/api/transactions')
def get_transactions():
   validation = validate(request)
   if validation["status"] != 200:
      return validation["message"], validation["status"]
   return transactions[validation["id"]]

if (__name__ == "__main__"):
   setup()
   app.run()
