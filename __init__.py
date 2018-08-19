from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/brocks/boost/db/boost.db'
    app.config['SECRET_KEY'] = 'savage12'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    return app

def create_db(app):
    db = SQLAlchemy(app)
    db.init_app(app)

    return db