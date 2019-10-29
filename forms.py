from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, length

class UserForm(FlaskForm):
    uname = StringField('Username', \
            validators=[DataRequired()])
    pword = PasswordField('Password', \
            validators=[DataRequired(), length(min=8)])
    twofa = StringField('Phone number', id='2fa', \
            validators=[length(min=9)])
