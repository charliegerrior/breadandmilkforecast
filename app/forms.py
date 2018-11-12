from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, HiddenField, SubmitField
from wtforms.validators import DataRequired,Regexp

class QueryForm(FlaskForm):
  zip_code = StringField('zip code', validators=[DataRequired(),Regexp("^[0-9]{5}$",flags=0,message="Please enter a valid 5 digit US zip code")])
  bread = BooleanField('bread', default="checked")
  eggs = BooleanField('eggs')
  milk = BooleanField('milk', default="checked")
  tp = BooleanField('toilet paper')
  submit = SubmitField('submit')

class RegistrationForm(FlaskForm):
  name = StringField('your name', validators=[DataRequired()])
  number = StringField('cell phone number', validators=[DataRequired(),Regexp("^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$",flags=0,message="Please enter a valid 10 digit US phone number")])
  region = HiddenField('region')
  submit = SubmitField('sign up')

  def validate_number(self, number):
    user = User.query.filter_by(number=number.data).first()
    if user is not None:
      raise ValidationError('Please use a different number.')


