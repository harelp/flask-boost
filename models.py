from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_socketio import SocketIO
import datetime

db = SQLAlchemy()
socketio = SocketIO()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    role = db.Column(db.String(80))

'''class ChatLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chatid = db.Column(db.Integer)
    message = db.Column(db.String(100))
    user_id = db.Column(db.String(20))
    created_date = db.Column(DateTime(timezone=True))
'''

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_type = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)