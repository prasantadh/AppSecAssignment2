from flask import Flask
from flask_login import LoginManager, login_required, current_user
from os import urandom
from models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(24)
login = LoginManager(app)
login.view = 'login'

def load_user(uname):
    return User.get_id(uname)

@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('spell_check'))
    return "Register or Login"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('spell_check'))
    return "Login under construction"

@app.route('/spell_check', methods=['GET', 'POST'])
@login_required
def spell_check():
    return "We will be back with functionality soon"

if __name__=='__main__':
    app.run()



