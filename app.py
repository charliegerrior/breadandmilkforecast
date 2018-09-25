# Import Flask and brickseek library
from flask import Flask, jsonify
from flask import request
from flask import redirect
from brickseek import *
from stats import *

app = Flask(__name__, static_folder='public', static_url_path='')
#skus = [13033157, 145051970, 10450115]

staples = [{'name' : 'milk', 'sku' : 10450115}, {'name' : 'eggs', 'sku' : 145051970}, {'name' : 'bread', 'sku' : 13033157}]

# POST route to handle a new form
@app.route("/api/query/new", methods=['POST'])
def new_query():
  items = {}
  for staple in staples:
    # We'll wrap this in a try to catch any API
    # errors that may occur
    try:
      bs_results = getStats(getInventory(staple['sku'],request.form['zip_code']))
      items[staple['name']] = bs_results
      #items.append(bs_results)
    except:
      print("ERROR!")

  return jsonify(items), 201

if __name__ == "__main__":
  app.run('192.168.1.14', 9001)
