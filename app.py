# Import Flask and brickseek library
from flask import Flask, jsonify
from flask import request
from flask import redirect
from brickseek import *
from stats import *

app = Flask(__name__, static_folder='../../public', static_url_path='')
skus = [13033157, 145051970, 10450115]


# POST route to handle a new subscription form
@app.route("/api/query/new", methods=['POST'])
def new_query():
  items = []
  for sku in skus:
    # We'll wrap this in a try to catch any API
    # errors that may occur
    try:
      item = getStats(getInventory(sku,request.form['zip_code']))
      items.append(item)
    except:
      print("ERROR!")

  return jsonify({'results' : items}), 201

if __name__ == "__main__":
  app.run('127.0.0.1', 9001)
