import os, sys, uuid

SECRET_KEY = uuid.uuid4().bytes
DEBUG=True

HOSTNAME = 'http://localhost:5555'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# database_server
SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/brocks/boost/db/boost.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True