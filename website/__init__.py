from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from . import constants

# for the login system
from flask_login import LoginManager, login_manager

# Config the database
db = SQLAlchemy()
DB_Name = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5567 6537'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_Name}'
    app.config['UPLOAD_FOLDER'] = os.getcwd()

    # define the place to store img website\static\images
    IMG_FOLDER = os.path.join('website', 'static', 'images')
    app.config['IMG_FOLDER'] = IMG_FOLDER

    # apply the database in this app
    db.init_app(app)


    from .views import views
    from .auth import auth
    from .reports import reports

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(reports, url_prefix='/')

    # import the database structure and create the database
    from .models import User, Record, ExploreNew
    database_create(app)

    # Initalizing the app and set up with the login page
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # load with the user record
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
        
    return app


def database_create(app):
    # define the location of database
    if not path.exists('website/' + DB_Name):
        db.create_all(app = app)
        print(constants.DATABASE_SUCCESS_MSG)