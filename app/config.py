from environs import Env

env = Env()
env.read_env()

ENV = env.str("FLASK_ENV", default="development")
DEBUG = ENV == "development"
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URI")
SECRET_KEY = env.str("SECRET_KEY")
SQLALCHEMY_TRACK_MODIFICATIONS = False 