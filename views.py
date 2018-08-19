from flask import Flask, render_template, redirect, url_for, Blueprint, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy, functools
from sqlalchemy import func
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from passlib.hash import sha256_crypt
from boostforms import LoginForm, RegisterForm
from .models import User

mainbp = Blueprint('mainbp', __name__, template_folder='templates', static_folder='static')


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
        
        if user:
            if user.username.lower() == submitted_username.lower():
                if sha256_crypt.verify(form.password.data, user.password):
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

@mainbp.route('/userdashboard')
@login_required
def userdashboard():
    return render_template('userdashboard.html', name=current_user.username)

@mainbp.route('/chat')
@login_required
def usertobooster_chat():
    return render_template('usertobooster.html', name=current_user.username)