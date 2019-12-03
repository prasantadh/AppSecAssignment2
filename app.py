# library imports
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_required, current_user, login_user
from os import urandom
from subprocess import Popen, PIPE, STDOUT
from werkzeug.security import generate_password_hash, check_password_hash

# imports from local files
from models import User
from forms import UserForm, SpellForm

# global settings
app = Flask(__name__)
## app.config.from_object('config')
app.config['SECRET_KEY'] = urandom(32)
login = LoginManager(app)
login.login_view = 'login'
login.session_protection = "strong"

# setup sqlite database for users
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
from models import db
db.init_app(app)

@login.user_loader
def load_user(user_id):
    with app.app_context():
        return User.query.get(int(user_id))

@app.after_request
def apply_caching(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

# parse data from the incoming requests
def get_data(request):
    uname = request.form['uname']
    pword = request.form['pword']
    twofa = None
    if 'twofa' in request.form.keys():
        twofa = request.form['twofa']
    return uname, pword, twofa

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    message = None
    if form.validate_on_submit():
        uname, pword, twofa = get_data(request)
        with app.app_context():
            if User.query.filter(User.uname==uname).first() is not None:
                message = 'Registration failure! Username taken!'
            else:
                user = User(uname, pword, twofa)
                db.session.add(user)
                db.session.commit()
                message = 'Registration success! Login to continue'
    elif request.method == 'POST':
        message = 'Registration failure!'
    return render_template('register.html', form=form, message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm()
    message = None if request.method == 'GET' else 'Incorrect username/password'
    if form.validate_on_submit():
        uname, pword, twofa = get_data(request)
        with app.app_context():
            user = User.query.filter(User.uname == uname).first()
            if user is not None:
                if check_password_hash(user.pword, pword) and user.twofa == twofa:
                    user.is_authenticated = True
                    db.session.commit()
                    login_user(user)
                    message = 'Login success'
                elif user.twofa != twofa:
                    message = 'Two-factor failure!'
    return render_template('login.html', form=form, message=message)

@app.route('/spell_check', methods=['GET', 'POST'])
@login_required
def spell_check():
    textout = None
    misspelled = None
    form = SpellForm()
    if form.validate_on_submit():
        textout = request.form['inputtext']
        filename = urandom(32).hex()
        f = open(filename, 'w')
        f.write(textout)
        f.close()
        stdout, stderr = Popen(['./a.out', filename, 'wordlist.txt'],
            stdout=PIPE, stderr=STDOUT).communicate()
        misspelled = stdout.decode().replace('\n',',')
        p = Popen(['rm', filename], stdout=PIPE, stderr=STDOUT)

    return render_template('spell_check.html', \
            form=form, textout=textout,misspelled=misspelled)


if __name__=='__main__':
    app.run()

