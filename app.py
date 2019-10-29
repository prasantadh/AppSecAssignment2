# library imports
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_required, current_user
from os import urandom

# imports from local files
from models import User
from forms import UserForm

# global settings
app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(24)
login = LoginManager(app)
login.view = 'login'
users = {} #our make-do database for users

def load_user(uname):
    return User.get_id(uname)

# parse data from the incoming requests
def get_data(request):
    uname = request.form['uname']
    pword = request.form['pword']
    twofa = None
    if '2fa' in request.form.keys():
        twofa = request.form['2fa']
    return uname, pword, twofa

@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('spell_check'))
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    message = None
    return render_template('register.html', form=form, message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm()
    message = None
    return render_template('login.html', form=form, message=message)

@app.route('/spell_check', methods=['GET', 'POST'])
@login_required
def spell_check():
    return "We will be back with functionality soon"

if __name__=='__main__':
    app.run()



