from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "e59ba2ff39ea91d95a57de87558ec8a5"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app) 
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)
loginManager.login_view = "logisn"
loginManager.login_message_category = "info"

from flaskShell import routes