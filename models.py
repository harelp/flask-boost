from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_socketio import SocketIO, join_room
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
    room = db.Column(db.String(20))

    def __init__(self, message, userfrom, created_date, room="None"):
        self.message = message
        self.userfrom = userfrom
        self.created_date = created_date
        self.room = room

class Booster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booster_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    join_date = db.Column(db.DateTime(timezone=True))
    current_order = db.Column(db.Integer, db.ForeignKey('orders.id'))
    current_balance = db.Column(db.Float)

    def __init__(self, booster_name, email, password, join_date):
        self.booster_name = booster_name
        self.password = password
        self.email = email
        self.join_date = join_date
        

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_type = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_amount = db.Column(db.Float, nullable=False)
    booster_assigned = db.Column(db.String(20), db.ForeignKey('booster.booster_name'))

    def __init__(order_type, user_id, order_amount, booster_assigned="None"):
        self.message = message
        self.userfrom = userfrom
        self.created_date = created_date
        self.booster_assigned = booster_assigned