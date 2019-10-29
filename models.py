from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, uname, pword, twofa):
        self.uname = uname
        self.pword = check_password_hash(pword)
        self.twofa = generate_password_hash(twofa)
        self.authenticated = True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.uname

    def is_authenticated(self):
        return self.authenticated

    def authenticate(self, uname, pword, twofa):
        if uname == self.uname and check_password_hash(self.pword, pword)\
                and twofa == self.twofa:
                    self.authenticated = True
