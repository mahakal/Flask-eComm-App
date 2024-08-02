from flask import Flask, render_template

from app import user
from app.command import init_db
from app.database import db
from app.extensions import bcrypt,login_manager

from app.models import *
from app.product.models import *


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
        return user.model.User.query.get(int(user_id))

def register_blueprint(app):
    app.register_blueprint(user.views.blueprint)

def register_commands(app):
    app.cli.add_command(init_db)
