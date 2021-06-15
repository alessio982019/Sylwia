
from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_util_js import FlaskUtilJs
from flask_mail import Mail
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = "onlineshop420it@gmail.com"
app.config['MAIL_PASSWORD'] = "Admin123!"
app.config['MAIL_DEFAULT_SENDER'] = "onlineshop420it@gmail.com"
app.config['MAIL_MAX_EMAILS'] = 1
app.config['MAIL_ASCII_ATTACHMENTS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'main/static/images')
mail=Mail(app)

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


TEMPLATES_AUTO_RELOAD = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
fujs = FlaskUtilJs(app)
app.config['SECRET_KEY'] = 'ec1284e00372b1e61bb6ab3032650192'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view ='login'
login_manager.login_message_category = 'info'

import main.routes
