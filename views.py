from flask import Flask, render_template, redirect, url_for, Blueprint, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy, functools
from sqlalchemy import func
from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, BooleanField
from passlib.hash import sha256_crypt
from .boostforms import LoginForm, RegisterForm, SoloOrderForm
from .models import User, db, socketio, ChatLog, Orders, join_room, Booster
import datetime

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
                else:
                     return '<h1> You\'re stupid </h1>'
            else:
                return '<h1> Invalid Login </h1>'
        else:
            return '<h1> Invalid Login </h1>'
    return render_template('login.html', form=form)


@mainbp.route('/boosterlogin', methods=["GET", "POST"])
def boosterlogin():
    form = LoginForm()

    if form.validate_on_submit():
        submitted_username = form.username.data
        submitted_username = str(submitted_username)
        submitted_username = submitted_username.lower()

        booster = Booster.query.filter(func.lower(Booster.booster_name)==submitted_username).first()
        print (booster.booster_name)
        if booster:
            print (booster.password)
            print (form.password.data)
            if booster.booster_name.lower() == submitted_username.lower():
                if sha256_crypt.verify(form.password.data, booster.password):
                    login_user(booster, remember=form.remember.data)
                    return redirect(request.args.get('next') or url_for('.index'))
                else:
                     return '<h1> Wrong Password </h1>'
            else:
                return '<h1> Invalid Login </h1>'
        else:
            return '<h1> Invalid Login </h1>'

    return render_template('boosterlogin.html', form=form)


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
    print (request.sid)
    username = json['user_name']
   
    
    send_to = Orders.query.filter(Orders.booster_assigned=="booster").first()

    roomtosend = users[send_to.booster_assigned]
    print (roomtosend)
    print (request.sid)
    print (send_to.booster_assigned)
    #Need Logic to put booster and Client in room
    msg = ChatLog(json['message'], current_user.username, datetime.datetime.now(), room=roomtosend)

    socketio.emit('display_to_chat', json, room="room1", callback=message_received)
    db.session.add(msg)
    db.session.commit()
    
def handle_join_room(room):
    join_room(room)