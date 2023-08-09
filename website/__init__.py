from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from os import path

db = SQLAlchemy()

def create_app():
    port = os.getenv('PORT', '3306')
    host = os.getenv('HOST', '172.17.0.2')
    password = os.getenv('PASSWORD', 'noabt2410')
    db_user = os.getenv('DB_USER', 'root')
    db_name = os.getenv('DB_NAME', 'dsm')

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'super-duper-secret-key-that-no-one-will-know-noderet-neder'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{db_user}:{password}@{host}:{port}/{db_name}'
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Student, Lesson

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app








