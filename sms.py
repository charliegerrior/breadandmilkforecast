from twilio.rest import Client
# Your Account SID from twilio.com/console
account_sid = "AC2d05a2524c9ef97454cf6cc1c2f8923a"
# Your Auth Token from twilio.com/console
auth_token = "d22db277cdb9f52de549e198acf39677"

client = Client(account_sid, auth_token)

def sendWelcome(user):
  message = client.messages.create(
    to="+1%s" % user['number'],
    from_="+17745653043",
    body="Hello %s! Thanks for registering in %s!" % (user['name'], user['region']))

  return message.sid
