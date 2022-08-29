import os
from pathlib import Path
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()

login_manager.login_view = 'auth.signup'
login_manager.login_message = ''

def create_app():
	app = Flask(__name__)

	app.config.from_mapping(
		SECRET_KEY = os.environ.get('SECRET_KEY'),
		SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI'),
		SQLALCHEMY_TRACK_MODIFICATIONS = bool(os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')),
		SQLALCHEMY_ECHO = bool(os.environ.get('SQLALCHEMY_ECHO')),
		WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY'),
	)

	csrf.init_app(app)
	db.init_app(app)
	Migrate(app, db)
	login_manager.init_app(app)

	from apps.crud import views as crud_views
	app.register_blueprint(crud_views.crud, url_prefix='/crud')

	from apps.auth import views as auth_views
	app.register_blueprint(auth_views.auth, url_prefix='/auth')

	return app




