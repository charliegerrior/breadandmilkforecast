from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class QueryForm(FlaskForm):
    zip_code = StringField('zip code')
    bread = BooleanField('bread', default="checked")
    eggs = BooleanField('eggs')
    milk = BooleanField('milk', default="checked")
    tp = BooleanField('toilet paper')
    submit = SubmitField('submit')

class SmsForm(FlaskForm):
  name = StringField('your name')
  number = StringField('cell phone number')
  submit = SubmitField('sign up')
