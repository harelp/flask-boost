import sys
from flask import Flask, render_template, redirect, url_for
from flask_script import Manager, Server
sys.path.append("/Users/brocks/boost/")
from fboost import create_app
from fboost.models import db
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView

app = create_app()

manager = Manager(app)

if __name__ == '__main__':
    app.debug = True
    app.run()