# Import Flask and brickseek library
from flask import Flask, jsonify, render_template
from flask import request
from flask import redirect
from brickseek import *
from stats import *

app = Flask(__name__, static_folder='public', static_url_path='')

staples = {'milk' : 10450115, 'eggs' : 145051970, 'bread' :  13033158}

#GET route to handle '/'
@app.route("/")
def home():
  return render_template('index.html')

# POST route to handle a new form
@app.route("/results.html", methods=['POST'])
def new_query():
  #print(request.form)
  items = []
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
      bs_results["name"] = selection
      items.append(bs_results)
    except:
      print("ERROR!")

  #return jsonify(items), 201
  print(items)

  return render_template('results.html', items=items)

#@app.route('/results.html')
#def results():
#  return render_template('results.html')

if __name__ == "__main__":
  app.run('0.0.0.0', 9001, debug=True)
