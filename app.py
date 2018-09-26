# Import Flask and brickseek library
from flask import Flask, jsonify
from flask import request
from flask import redirect
from brickseek import *
from stats import *

app = Flask(__name__, static_folder='public', static_url_path='')
#skus = [13033157, 145051970, 10450115]

staples = {'milk' : 10450115, 'eggs' : 145051970, 'bread' :  13033157}

# POST route to handle a new form
@app.route("/api/query/new", methods=['POST'])
def new_query():
  #print(request.form)
  items = {}
  selections = []
  if 'item1' in request.form:
    selections.append(request.form['item1'])
  if 'item2' in request.form:
    selections.append(request.form['item2'])
  if 'item3' in request.form:
    selections.append(request.form['item3'])
  #print(selections)
  for selection in selections:
    # We'll wrap this in a try to catch any API
    # errors that may occur
    try:
      bs_results = getStats(getInventory(staples[selection],request.form['zip_code']))
      items[selection] = bs_results
      #items.append(bs_results)
    except:
      print("ERROR!")

  return jsonify(items), 201

if __name__ == "__main__":
  app.run('192.168.1.14', 9001, debug=True)
