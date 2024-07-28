from flask import Flask, render_template

from app import user
from app.command import init_db
from app.database import db
from app.extensions import bcrypt


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

def register_blueprint(app):
    app.register_blueprint(user.views.blueprint)

def register_commands(app):
    app.cli.add_command(init_db)
