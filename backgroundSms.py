from twilio.rest import Client
from app import db
from app.models import User, Forecast
from forecast import *

from datetime import datetime, timedelta

# Your Account SID from twilio.com/console
account_sid = "AC2d05a2524c9ef97454cf6cc1c2f8923a"
# Your Auth Token from twilio.com/console
auth_token = "d22db277cdb9f52de549e198acf39677"

client = Client(account_sid, auth_token)

def sendAlert(user):
  message = client.messages.create(
    to="+1%s" % user.number,
    from_="+17745653043",
    body="Hello %s! This message is to alert you that inventory levels in %s are dropping!" % (user.name, user.region))

  return message.sid


users = User.query.all()

for user in users:
  forecast = Forecast.query.filter_by(region=user.region).first()
  if datetime.utcnow() - forecast.timestamp > timedelta(seconds=1800):
    forecast = getForecast(forecast.region)
    #write to DB
  else:
    if (forecast.bread_percent > 0 or forecast.eggs_percent > 0 or forecast.milk_percent > 0 or forecast.tp_percent > 0):
      sendAlert(user)
