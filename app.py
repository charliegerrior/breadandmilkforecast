# Import Flask and brickseek library
from flask import Flask, jsonify, render_template
from flask import request
from flask import redirect
from brickseek import *
from stats import *
import re

app = Flask(__name__, static_folder='public', static_url_path='')

staples = {'milk' : 10450115, 'eggs' : 145051970, 'bread' :  120099533}

#GET route to handle '/'
@app.route("/")
def home():
  return render_template('index.html')

#GET route to handle '/legal.html'
@app.route("/legal.html")
def legal():
  return render_template('legal.html')

#GET route to handle '/about.html'
@app.route("/about.html")
def about():
  return render_template('about.html')

# POST route to handle a new form
@app.route("/results.html", methods=['POST'])
def new_query():
  matchObj = re.match(r'^[0-9]{5}$', request.form['zip_code'])
  selections = []
  if 'item1' in request.form:
    selections.append(request.form['item1'])
  if 'item2' in request.form:
    selections.append(request.form['item2'])
  if 'item3' in request.form:
    selections.append(request.form['item3'])

  if matchObj and len(selections) > 0:
    items = []
    for selection in selections:
      # We'll wrap this in a try to catch any API
      # errors that may occur
      try:
        bs_results = getStats(getInventory(staples[selection],request.form['zip_code']))
        bs_results["name"] = selection
        items.append(bs_results)
      except:
        print("ERROR!")

    return render_template('results.html', items=items)

  else:
   return render_template('error.html')

if __name__ == "__main__":
  app.run('0.0.0.0', 9001)
