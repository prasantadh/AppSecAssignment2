from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

class User:
    def __init__(self, uname=None, pword=None, twofa=None):
        self.uname = uname
        self.pword = generate_password_hash(pword, \
                        method='pbkdf2:sha256:150000', salt_length=16)
        self.twofa = twofa
        self.is_authenticated = False
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return self.uname

    def authenticate(self, uname, pword, twofa):
        if (self.uname != uname or not check_password_hash(self.pword, pword)):
            return 'Incorrect username/password!'
        if (self.twofa != twofa):
            return 'Two-factor failure!'
        self.is_authenticated = True
        login_user(self)
        return 'Login success'

    def __str__(self):
        return "uname : {}\n pword: {}\n  2fa: {}\n authenticated: {}\n"\
                .format(self.uname, self.pword, self.twofa, self.authenticated)
