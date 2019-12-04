from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, length

class UserForm(FlaskForm):
    uname = StringField('Username', \
            validators=[DataRequired(), length(max=120)])
    pword = PasswordField('Password', \
            validators=[DataRequired(), length(min=8)])
    twofa = StringField('Phone number', id='2fa', \
            validators=[length(min=9)])

class SpellForm(FlaskForm):
    inputtext = TextAreaField('Text to check', \
            validators=[DataRequired(), length(min=1, max=120)])

class UnameForm(FlaskForm):
    uname = StringField('Username', \
            validators=[DataRequired(), length(max=120)])