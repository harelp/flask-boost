from flask import Flask, redirect, request
from flask_bootstrap import Bootstrap
from fboost.models import db
from fboost import views

def create_app():

    app = Flask(__name__)
    app.config.from_object('config')

    #Setup the database
    from flask_sqlalchemy import SQLAlchemy
    
    db.init_app(app)

    from .views import mainbp
    app.register_blueprint(views.mainbp)

    from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = '.login'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    Bootstrap(app)

    return app