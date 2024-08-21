# ruff: noqa: F403
from flask import Flask

from app.command import init_db
from app.database import db
from app.extensions import bcrypt, login_manager
from app.index.views import bp as IndexBP
from app.models import *
from app.product.views import bp as ProductBp
from app.user.models import User
from app.user.views import bp as UserBp
from app.user_profile.views import bp as UserProfileBp


def create_app(config_object="app.config"):
	app = Flask(__name__)
	app.config.from_object(config_object)
	register_extension(app)
	register_blueprint(app)
	register_commands(app)
	return app


def register_extension(app):
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(int(user_id))


def register_blueprint(app):
	app.register_blueprint(UserBp)
	app.register_blueprint(ProductBp)
	app.register_blueprint(UserProfileBp)
	app.register_blueprint(IndexBP)


def register_commands(app):
	app.cli.add_command(init_db)
