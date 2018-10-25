
from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    number = db.Column(db.String(64), index=True, unique=True)
    region = db.Column(db.String(5), index=True, unique=False)
    def __repr__(self):
        return '<User {}>'.format(self.name)

class Forecast(db.Model):
  region = db.Column(db.String(5), primary_key=True)
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  #eggs
  eggs_inv = db.Column(db.Integer, unique=False)
  eggs_stores  = db.Column(db.Integer, unique=False)
  eggs_distance = db.Column(db.Integer, unique=False)
  #bread
  bread_inv = db.Column(db.Integer, unique=False)
  bread_stores  = db.Column(db.Integer, unique=False)
  bread_distance = db.Column(db.Integer, unique=False)
  #milk
  milk_inv = db.Column(db.Integer, unique=False)
  milk_stores  = db.Column(db.Integer, unique=False)
  milk_distance = db.Column(db.Integer, unique=False)
  #tp
  tp_inv = db.Column(db.Integer, unique=False)
  tp_stores  = db.Column(db.Integer, unique=False)
  tp_distance = db.Column(db.Integer, unique=False)

  def __repr__(self):
    return '<Forecast {}>'.format(self.region)
