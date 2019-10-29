from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

class User:
    def __init__(self, uname=None, pword=None, twofa=None):
        self.uname = uname
        self.pword = generate_password_hash(pword)
        self.twofa = twofa
        self.authenticated = False

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.uname

    def is_authenticated(self):
        return self.authenticated

    def authenticate(self, uname, pword, twofa):
        if (self.uname != uname or not check_password_hash(self.pword, pword)):
            return 'Incorrect username/password!'
        if (self.twofa != twofa):
            return 'Two-factor failure!'
        self.authenticated = True
        login_user(self)
        return 'Login success'

    def __str__(self):
        return "uname : {}\n pword: {}\n  2fa: {}\n authenticated: {}\n"\
                .format(self.uname, self.pword, self.twofa, self.authenticated)
