from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bcec6cfc03974b3fdb9e87253e03d977'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manger = LoginManager(app)
login_manger.login_view = 'login'
login_manger.login_message_category = 'warning'

from flaskblog import routes
