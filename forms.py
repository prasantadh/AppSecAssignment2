from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, length
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename

class UserForm(FlaskForm):
    uname = StringField('Username', \
            validators=[DataRequired()])
    pword = PasswordField('Password', \
            validators=[DataRequired(), length(min=8)])
    twofa = StringField('Phone number', id='2fa', \
            validators=[length(min=9)])

class SpellForm(FlaskForm):
    inputtext = TextAreaField('Text to check', \
            validators=[DataRequired()])

