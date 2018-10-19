from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, HiddenField, SubmitField
from wtforms.validators import DataRequired

class QueryForm(FlaskForm):
<<<<<<< HEAD
  zip_code = StringField('zip code')
  bread = BooleanField('bread', default="checked")
  eggs = BooleanField('eggs')
  milk = BooleanField('milk', default="checked")
  tp = BooleanField('toilet paper')
  submit = SubmitField('submit')

class RegistrationForm(FlaskForm):
  name = StringField('your name', validators=[DataRequired()])
  number = StringField('cell phone number', validators=[DataRequired()])
  region = HiddenField('region')
  submit = SubmitField('sign up')

  def validate_number(self, number):
    user = User.query.filter_by(number=number.data).first()
    if user is not None:
      raise ValidationError('Please use a different number.')
=======
    zip_code = StringField('zip code')
    bread = BooleanField('bread', default="checked")
    eggs = BooleanField('eggs')
    milk = BooleanField('milk', default="checked")
    tp = BooleanField('toilet paper')
    submit = SubmitField('submit')

class SmsForm(FlaskForm):
  name = StringField('your name')
  number = StringField('cell phone number')
  submit = SubmitField('submit')
>>>>>>> adds form for txt signup and receives input
