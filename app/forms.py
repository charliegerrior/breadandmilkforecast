from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class QueryForm(FlaskForm):
    zip_code = StringField('zip code', validators=[DataRequired()])
    bread = BooleanField('bread')
    eggs = BooleanField('eggs')
    milk = BooleanField('milk')
    tp = BooleanField('toilet paper')
    submit = SubmitField('submit')
