from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_socketio import SocketIO
import datetime

db = SQLAlchemy()
socketio = SocketIO()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    role = db.Column(db.String(80))

class ChatLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100), nullable=False)
    userfrom = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)
    created_date = db.Column(db.DateTime(timezone=True))

    def __init__(self, message, userfrom, created_date):
        self.message = message
        self.userfrom = userfrom
        self.created_date = created_date
        

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_type = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_amount = db.Column(db.Float, nullable=False)