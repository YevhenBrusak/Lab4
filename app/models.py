from . import bcrypt
from . import db
import os, base64, onetimepass as otp

class User(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    totp_secret = db.Column(db.String(16))

    def __repr__(self):
        return f"User : {self.username}, Email: {self.email}"

    @property
    def password_hash(self):
        raise AttributeError('Is not readable')

    @password_hash.setter
    def password_hash(self, password_hash):
        self.password = bcrypt.generate_password_hash(password_hash)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = password
        if self.totp_secret is None:
            self.totp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')
    
    def verify_password(self, password_hash):
        return bcrypt.check_password_hash(self.password, password_hash)
    
    def get_totp_uri(self):
        return f'otpauth://totp/TOTPDemo:{self.username}?secret={self.totp_secret}&issuer=TOTPDemo'

    def verify_totp(self, token):
        return otp.valid_totp(token, self.totp_secret)