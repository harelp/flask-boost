from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length

leagues = [('Bronze 5', 'Bronze 5'), ('Bronze 4', 'Bronze 4'), ('Bronze 3','Bronze 3')]

#Need a list of tuples


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[InputRequired(), Length(min=4, max=20)],render_kw={"placeholder": "Username"})
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=8, max=80)],render_kw={"placeholder": "Password"})
    remember = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


class SoloOrderForm(FlaskForm):
    current_rank = SelectField(label='Current Rank', choices=leagues)
