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
      app.logger.info('No forecast for %s in database' % (region))
      # We'll wrap this in a try to catch any errors that may occur
      app.logger.info('Retrieving forecast for %s from Brickseek' % (region))
      try:
        forecast = getForecast(region)
      except:
        app.logger.warning('Unable to retrieve forecast for %s from Brickseek' % (region))
     #write forecast to DB
      try:
        addForecast(forecast)
      except:
        app.logger.warning('Could not write forecast to DB')

    elif datetime.utcnow() - db_forecast.timestamp > timedelta(seconds=1800):
      app.logger.info('No forecasts for %s within the past 30 minutes. Retrieveing a fresh forecast from Brickseek' % (region))
      try:
        forecast = getForecast(region)
      except:
        app.logger.warning('Unable to retrieve forecast for %s from Brickseek' % (region))
      #update existing forecast
      try:
        updateForecast(db_forecast, forecast)
      except:
        app.logger.warning('Could not write forecast to DB')
    else:
      #retrieve from DB
      app.logger.info('Using forecast retrieved from DB')
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
  app.logger.info('Adding user %s with number %s to DB' % (user.name, user.number))
  try:
    db.session.add(user)
    db.session.commit()
    user = { 'name': request.form['name'], 'number': request.form['number'], 'region': request.form['region'] }
    app.logger.info('Sending welcome message to %s' % (user['number']))
    try:
      sendWelcome(user)
    except:
      app.logger.warning('Could not send message to %s' % (user['number']))
      return render_template('error.html')
  except:
    app.logger.warning('Could not add user to DB')
    return render_template('error.html')

  return render_template('signup.html', user=user)


