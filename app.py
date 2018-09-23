# Import Flask and brickseek library
from flask import Flask, jsonify
from flask import request
from flask import redirect
from brickseek import *
from stats import *

app = Flask(__name__, static_folder='../../public', static_url_path='')

# POST route to handle a new subscription form
@app.route("/api/query/new", methods=['POST'])
def new_query():

  # We'll wrap this in a try to catch any API
  # errors that may occur
  try:
    item = getStats(getInventory(10450115,request.form['zip_code']))
    #print(item)
  except:

    # Here we may wish to log the API error and send the
    # customer to an appropriate URL, perhaps including
    # and error message. See the `error_redirect` and
    # `compose_errors` functions below.
    #error_redirect(compose_errors(errors))
    print("ERROR!")

  return jsonify(item), 201

# A few utility functions for error handling
def error_redirect(message):
  redirect('ERROR_URL?errors=' + message)

def compose_errors(errors):
  ', '.join(e.message for e in errors)

if __name__ == "__main__":
  app.run('127.0.0.1', 9001)
