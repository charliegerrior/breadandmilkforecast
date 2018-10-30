from flask import Flask
from config import Config

import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__, static_folder='public', static_url_path='')
app.config.from_object(Config)

from app import routes, errors

if not app.debug:
  if not os.path.exists('logs'):
    os.mkdir('logs')
  file_handler = RotatingFileHandler('logs/breadandmilkforecast.log', maxBytes=10240, backupCount=10)
  file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
  file_handler.setLevel(logging.INFO)
  app.logger.addHandler(file_handler)
  app.logger.setLevel(logging.INFO)
  app.logger.info('Bread and Milk Forecast startup')
