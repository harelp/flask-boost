import sys
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy, functools
from sqlalchemy import func
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
sys.path.append("/Users/brocks/boost/")
from fboost import create_app, create_db
from fboost.boostforms import LoginForm, RegisterForm
from passlib.hash import sha256_crypt
from flask_socketio import SocketIO

app = create_app()
db = create_db(app)
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

Bootstrap(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        submitted_username = form.username.data
        submitted_username = str(submitted_username)
        submitted_username = submitted_username.lower()

        app.logger.info(submitted_username)
        user = User.query.filter(func.lower(User.username)==submitted_username).first()

        
        if user:
            if user.username.lower() == submitted_username.lower():
                if sha256_crypt.verify(form.password.data, user.password):
                    login_user(user, remember=form.remember.data)
                    return redirect(url_for('userdashboard'))
                else:
                     return '<h1> You\'re stupid </h1>'
            else:
                return '<h1> Invalid Login </h1>'
        else:
            return '<h1> Invalid Login </h1>'
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hash_password = sha256_crypt.hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/userdashboard')
@login_required
def userdashboard():
    return render_template('userdashboard.html', name=current_user.username)

@app.route('/chat')
@login_required
def usertobooster_chat():
    return render_template('usertobooster.html', name=current_user.username)

def messageReceived(methods=['GET', 'POST']):
    print ('message received')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('Received event ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    app.run(debug=True)
    socketio.run(app, debug=True)