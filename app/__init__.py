from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_recaptcha import ReCaptcha


app = Flask(__name__) 
app.config.from_object('config')
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
recaptcha = ReCaptcha(app=app)
app.config.update(dict(
    RECAPTCHA_ENABLED = True,
    RECAPTCHA_SITE_KEY = "6LfY3M8oAAAAANPruTIIw6NeeKM9x_0I0OI8p7i_",
    RECAPTCHA_SECRET_KEY = "6LfY3M8oAAAAAP8isVg77Y2MTqhmpn1MBnl45IAK",
))
recaptcha = ReCaptcha()
recaptcha.init_app(app)
app.app_context().push()
migrate = Migrate(app, db, render_as_bath=True)




from app import views, models