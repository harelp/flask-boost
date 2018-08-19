from flask_sqlalchemy import SQLAlchemy, functools
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from fboost import app

db = SQLAlchemy(app)
db.init_app(app)