from flask import Flask, redirect, request
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView

from passlib.hash import sha256_crypt
from flask_socketio import SocketIO, send, emit, join_room

import settings as settings

app = Flask(__name__)
app.config.from_object(settings)

#Setup the database
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

Bootstrap(app)

#Setup Login Manager - Sets default login view to /login

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '.login'

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def load_booster(booster_id):
    return Booster.query.get(int(booster_id))

#Setup Chat SocketIO
socketio = SocketIO()
socketio.init_app(app)


#Setup Flask-Admin

admin = Admin(app, name='fboost-admin')

class UserView(ModelView):
    column_exclude_list = ['password']
    column_display_pk = True
    can_create = True
    can_edit = True
    can_delete = True


    def on_model_change(self, form, model, is_created):
        model.password = sha256_crypt.hash(model.password)

    def is_accessible(self):
        return current_user.role == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return '<h1> You are not logged in!</h1>'

admin.add_view(UserView(User, db.session))

import views
app.register_blueprint(views.mainbp)
import models
import boostforms


if __name__ == '__main__':
    app.run()