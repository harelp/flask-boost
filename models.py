from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

import datetime
from quickboosters import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    role = db.Column(db.String(80))

    def __init__(self, username, email, password, role="None"):
        self.username = username
        self.email = email
        self.password = password
        self.role = role

class ChatRoom(db.Model):
    __tablename__ = 'chatroom'
    id = db.Column(db.Integer, primary_key=True)
    roomname = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, roomname):
        self.roomname = roomname

class ChatLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100), nullable=False)
    userfrom = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)
    created_date = db.Column(db.DateTime(timezone=True))
    room = db.Column(db.String(20), db.ForeignKey('chatroom.roomname'))

    def __init__(self, message, userfrom, created_date, room="None"):
        self.message = message
        self.userfrom = userfrom
        self.created_date = created_date
        self.room = room

'''class Booster_Attributes(db.Model):
    balance = db.Column(db.Float)
    current_order = db.Column(db.Integer, db.ForeignKey('orders.id'))
    booster_id = db.Column(db.Integer)

    def __init__(self, booster_id, current_order=0, balance=0):
        self.booster_id = booster_id
        self.currender_order = current_order
        self.balance = balance
  '''      

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_type = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_amount = db.Column(db.Float, nullable=False)
    booster_assigned = db.Column(db.String(20), db.ForeignKey('users.username'))

    def __init__(order_type, user_id, order_amount, booster_assigned="None"):
        self.message = message
        self.userfrom = userfrom
        self.created_date = created_date
        self.booster_assigned = booster_assigned