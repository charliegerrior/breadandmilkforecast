# Import Flask and brickseek library
from flask import render_template, request, redirect
from forecast import *
from sms import *
from datetime import datetime, timedelta
import re

from app import app, db
from app.models import User, Forecast
from app.forms import QueryForm, RegistrationForm

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
    region = request.args['zip_code']
    db_forecast = Forecast.query.filter_by(region=region).first()
    if db_forecast is None:
      #run new query
      print('no recent forecast in database')
      # We'll wrap this in a try to catch any API
      # errors that may occur
      try:
        forecast = getForecast(region)
      except:
        print("ERROR!")
      #write forecast to DB
      addForecast(forecast)
    elif datetime.utcnow() - db_forecast.timestamp > timedelta(seconds=1800):
      try:
        forecast = getForecast(region)
      except:
        print("ERROR!")
      #update existing forecast
      updateForecast(db_forecast, forecast)
    else:
      #retrieve from DB
      print('retrieving forecast from DB')
      forecast = convertForecast(db_forecast)
    form = RegistrationForm(region=region)
    return render_template('forecast.html', forecast=forecast, selections=selections, form=form)

  else:
   return render_template('error.html')

# POST route to handle a new sign up form
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
