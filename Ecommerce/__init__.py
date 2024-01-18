import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES, UploadSet, configure_uploads , patch_request_class
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
 
###################################
##### * DataBase Setup ############
###################################
app.config['SECRET_KEY'] = '0123456789abcdefghij'
app.config["SQLALCHEMY_DATABASE_URI"] =  'mysql+pymysql://aichaazlf:password123@localhost/Ecommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

###################################
##### * Handling Images ###########
###################################

migrate = Migrate(app, db)
with app.app_context():
    # Create the tables
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'customerLogin'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = u"Please Login Sir/ Madam"