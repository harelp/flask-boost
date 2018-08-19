import sys
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
sys.path.append("/Users/brocks/boost/")
from fboost import create_app

app = create_app()

if __name__ == '__main__':
    app.debug = True
    app.run()