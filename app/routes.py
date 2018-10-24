# Import Flask and brickseek library
from flask import render_template, request, redirect
from brickseek import *
from stats import *
import re

from app import app
from app.forms import QueryForm
staples = {'milk' : 10450115, 'eggs' : 145051970, 'bread' : 120099533, 'tp' : 549419637}

#GET route to handle '/'
@app.route("/")
def home():
  form = QueryForm()
  return render_template('index.html', form=form)

#GET route to handle '/legal'
@app.route("/legal")
def legal():
  return render_template('legal.html')

#GET route to handle '/about'
@app.route("/about")
def about():
  return render_template('about.html')

# POST route to handle a new form
@app.route("/results", methods=['POST'])
def results():
  matchObj = re.match(r'^[0-9]{5}$', request.form['zip_code'])
  selections = []
  if 'bread' in request.form:
    selections.append('bread')
  if 'eggs' in request.form:
    selections.append('eggs')
  if 'milk' in request.form:
    selections.append('milk')
  if 'tp' in request.form:
    selections.append('tp')

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
