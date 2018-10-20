# Import Flask and brickseek library
from flask import render_template, request, redirect
from brickseek import *
from stats import *
from sms import *
import re

<<<<<<< HEAD
from app import app, db
from app.models import User
from app.forms import QueryForm, RegistrationForm
=======
from app import app
from app.forms import QueryForm
<<<<<<< HEAD
from app.forms import SmsForm
>>>>>>> adds form for txt signup and receives input
=======
from app.forms import RegistrationForm
>>>>>>> working registration form with hidden zip code

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

# GET route to handle a new form
@app.route("/forecast", methods=['GET'])
def forecast():
  matchObj = re.match(r'^[0-9]{5}$', request.args['zip_code'])
  selections = []
  if 'bread' in request.args:
    selections.append('bread')
  if 'eggs' in request.args:
    selections.append('eggs')
  if 'milk' in request.args:
    selections.append('milk')
  if 'tp' in request.args:
    selections.append('tp')

  if matchObj and len(selections) > 0:
    items = []
<<<<<<< HEAD
    region = request.args['zip_code']
=======
    region = request.form['zip_code']
>>>>>>> working registration form with hidden zip code
    for selection in selections:
      # We'll wrap this in a try to catch any API
      # errors that may occur
      try:
        bs_results = getStats(getInventory(staples[selection],request.args['zip_code']))
        bs_results["name"] = selection
        items.append(bs_results)
      except:
        print("ERROR!")
<<<<<<< HEAD
<<<<<<< HEAD
    form = RegistrationForm(region=region)
    return render_template('forecast.html', items=items, form=form)
=======
    form = SmsForm()
=======
    form = RegistrationForm(region=region)
>>>>>>> working registration form with hidden zip code
    return render_template('results.html', items=items, form=form)
>>>>>>> adds form for txt signup and receives input

  else:
   return render_template('error.html')

# POST route to handle a new sign up form
<<<<<<< HEAD
@app.route("/signup", methods=['POST'])
def signup():
  form = request.form
  #if form.validate_on_submit():
  user = User(name=form['name'], number=form['number'], region=form['region'])
  db.session.add(user)
  db.session.commit()

  user = { 'name': request.form['name'], 'number': request.form['number'], 'region': request.form['region'] }
  sendWelcome(user)
  return render_template('signup.html', user=user)
  #return redirect(url_for('login'))
=======
@app.route("/signup.html", methods=['POST'])
<<<<<<< HEAD
def new_signup():
  return  render_template('signup.html')
>>>>>>> adds form for txt signup and receives input
=======
def register():
  user = { 'name': request.form['name'], 'number': request.form['number'], 'region': request.form['region'] }
  return  render_template('signup.html', user=user)

#if form.validate_on_submit():
#        user = User(name=form.name.data, number=form.number.data, region=)
#        db.session.add(user)
#        db.session.commit()
#        flash('Congratulations, you are now a registered user!')
#        return redirect(url_for('login'))
>>>>>>> working registration form with hidden zip code
