from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length

leagues = [('Bronze', 'Bronze'), ('Silver', 'Silver'), ('Gold','Gold'), ('Platinum', 'Platinum'), ('Diamond', 'Diamond')]

divisions = [('5', '5'), ('4', '4'), ('3', '3'), ('2', '2'), ('1','1')]
lp_choices = [('0-20', '0-20'), ('21-40', '21-40'), ('41-60', '41-60'), ('61-80', '61-80'), ('81-99', '81-99')]
class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[InputRequired(), Length(min=4, max=20)],render_kw={"placeholder": "Username"})
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=8, max=80)],render_kw={"placeholder": "Password"})
    remember = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class SoloOrderForm(FlaskForm):
    current_league = SelectField(label='Current League', choices=leagues)
    current_division = SelectField(label='Current Division', choices=divisions)
    current_lp = SelectField(label="Current lp", choices=lp_choices)

    desired_league = SelectField(label='Desired League', choices=leagues)
    desired_division = SelectField(label='Desired Division', choices=divisions)
    desired_lp = SelectField(label='Desired LP', choices=lp_choices)