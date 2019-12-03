from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(120), index=True, unique=True)
    pword = db.Column(db.String(120), nullable=False)
    twofa =  db.Column(db.String(120), nullable=True)
    is_active =  True
    is_anonymous = False
    is_authenticated = True

    def __init__(self, uname=None, pword=None, twofa=None):
        self.uname = uname
        self.pword = generate_password_hash(pword, \
                        method='pbkdf2:sha256:150000', salt_length=16)
        self.twofa = twofa

    def get_id(self):
        return self.id

    def __str__(self):
        return "uname : {}\n pword: {}\n  2fa: {}\n authenticated: {}\n"\
                .format(self.uname, self.pword, self.twofa, self.authenticated)

