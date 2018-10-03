from flask import Flask, render_template, redirect, url_for, Blueprint, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy, functools
from sqlalchemy import func
from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, BooleanField
from passlib.hash import sha256_crypt
from boostforms import LoginForm, RegisterForm, SoloOrderForm
from models import User, ChatLog, Orders, ChatRoom
from collections import OrderedDict
import datetime

from quickboosters import app, db, socketio

mainbp = Blueprint('mainbp', __name__, template_folder='templates', static_folder='static')

users = {}

@mainbp.route('/')
def index():
    return render_template('index.html')

@mainbp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        submitted_username = form.username.data
        submitted_username = str(submitted_username)
        submitted_username = submitted_username.lower()

        user = User.query.filter(func.lower(User.username)==submitted_username).first()
        print (user)
        if user:
            if user.username.lower() == submitted_username.lower():
                if sha256_crypt.verify(form.password.data, user.password) and user.role == "Admin":
                    login_user(user, remember=form.remember.data)
                    return redirect(request.args.get('next') or url_for('.admindashboard'))
                elif sha256_crypt.verify(form.password.data, user.password) and user.role == "Client":
                    login_user(user, remember=form.remember.data)
                    return redirect(request.args.get('next') or url_for('.userdashboard'))
                elif sha256_crypt.verify(form.password.data, user.password) and user.role == "None":
                    login_user(user, remember=form.remember.data)
                    return redirect(request.args.get('next') or url_for('.userdashboard'))
                else:
                     return '<h1> You\'re stupid </h1>'
            else:
                return '<h1> Invalid Login </h1>'
        else:
            return '<h1> Invalid Login </h1>'
    return render_template('login.html', form=form)


@mainbp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.index'))

@mainbp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hash_password = sha256_crypt.hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('.login'))

    return render_template('register.html', form=form)

@mainbp.route('/booster_register', methods=['GET', 'POST'])
def booster_register():
    form = RegisterForm()

    if form.validate_on_submit():
        booster_name = form.username.data
        hash_password = sha256_crypt.hash(form.password.data)
        email = form.email.data
        join_date = datetime.datetime.now()

        print ("booster_name: " + booster_name + " password: " + hash_password + " email: " + email)
        new_booster = Booster(booster_name=booster_name, email=email, password=hash_password, join_date=datetime.datetime.now())
        db.session.add(new_booster)
        db.session.commit()
        return redirect(url_for('.boosterlogin'))

    return render_template('booster_register.html', form=form)

@mainbp.route('/userdashboard')
@login_required
def userdashboard():
    return render_template('userdashboard.html', name=current_user.username)


@mainbp.route('/order', methods=['GET', 'POST'])
def order():
    form = SoloOrderForm()

    if form.validate_on_submit():
        current_league = form.current_league.data
        current_division = form.current_division.data
        current_lp = form.current_lp.data

        desired_league = form.desired_league.data
        desired_division = form.desired_division.data
        desired_lp = form.desired_lp.data

    return render_template('order.html', form=form)

@mainbp.route('/admindashboard')
@login_required
def admindashboard():
    return render_template('admindashboard.html', name=current_user.username)

@mainbp.route('/chat')
@login_required
def usertobooster_chat():
    return render_template('usertobooster.html', name=current_user.username)

@socketio.on('message')
@login_required
def received_message(message):
    print (current_user.username + " Connected To Chat.")
    users[current_user.username] = request.sid
def message_received(methods=['GET', 'POST']):
    print ('message received')


@socketio.on('client_msg')
@login_required
def handle_client_msg(json, methods=['GET', 'POST']):
    print (str(json))

    #Get the user who sent the msg
    user = User.query.filter(User.username == current_user.username).first()
    
    #Check to see if user is a client
    if current_user.username == user.username and user.role == "Client":
        booster = match_user_with_booster(user)
        
        #Create a room name
        roomname = str(current_user.username) + str(booster)
        cr = ChatRoom(roomname=roomname)

        try:
            db.session.add(cr)
            db.session.commit()
        finally:
            join_room(roomname)
            socketio.emit('display_to_chat', json, room=roomname, callback=message_received)

    elif user.role == "None": # Else was the user who sent the message a booster?
        user = match_booster_with_user(user)
        print ("User to booster"+ user)
        roomname = str(user) + str(current_user.username)
        roomtojoin = ChatRoom.query.filter(ChatRoom.roomname==roomname).first()
        print (roomtojoin)
        cr = ChatRoom(roomname=roomtojoin.roomname)

        print (roomtojoin.roomname)
        join_room(roomtojoin.roomname)
        socketio.emit('display_to_chat', json, room=roomname, callback=message_received)
    else:
        print (current_user.username)
        join_room(request.sid)

    try:
        msg = ChatLog(json['message'], current_user.username, datetime.datetime.now(), room=roomname)
    finally:
        db.session.add(msg)
        db.session.commit()
    
def handle_join_room(room):
    join_room(room)

#Returned a booster that is assigned to a user
def match_user_with_booster(user):
    print ("User sent MSG")
    order = Orders.query.filter(Orders.user_id==user.id).first()
    print ("order: " + order.booster_assigned)
    print ("SEnding to " + order.booster_assigned)
    return order.booster_assigned

#Returns a user that the booster is assigned to
def match_booster_with_user(booster):
    print ("Booster Sent MSG")
    order = Orders.query.filter(Orders.booster_assigned==booster.username).first()
    customer = User.query.filter(User.id==order.user_id).first()
    print ("Sending to " + customer.username)

    return customer.username

def determine_soloOrder_pricing():

    ranks = { 1 : 'Bronze 5', 2 : 'Bronze 4', 3 : 'Bronze 3', 4 : 'Bronze 2', 5 : 'Bronze 1',
     6 : 'Silver 5', 7 : 'Silver 4', 8 : 'Silver 3', 9 : 'Silver 2', 10 : 'Silver 1',
     11 : 'Gold 5', 12 : 'Gold 4', 13 : 'Gold 3', 14 : 'Gold 2', 15 : 'Gold 1',
     16 : 'Platinum 5', 17 : 'Platinum 4', 18 : 'Platinum 3', 19 : 'Platinum 2', 20 : 'Platinum 1',
     21 : 'Diamond 5', 22 : 'Diamond 4', 23 : 'Diamond 3', 24 : 'Diamond 2' , 25 : 'Diamond 1',
     26 : 'Master', 27 : 'Challenger'}

    one_league = 5
