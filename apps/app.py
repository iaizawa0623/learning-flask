from pathlib import Path
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
	app = Flask(__name__)

	app.config.from_mapping(
		SECRET_KEY='2AZSMss3p5QPbcY2hBs',
		SQLALCHEMY_DATABASE_URI=f'postgresql://postgres:jU3E|DaQ@localhost:5432/auto_irrigation',
		SQLALCHEMY_TRACK_MODIFICATIONS=False,
		SQLALCHEMY_ECHO=True,
		WTF_CSRF_SECRET_KEY='AuwzyszU5sugKN7KZs6f',
	)

	csrf.init_app(app)
	db.init_app(app)
	Migrate(app, db)

	from apps.crud import views as crud_views
	app.register_blueprint(crud_views.crud, url_prefix='/crud')

	return app




