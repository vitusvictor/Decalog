from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from decalog.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, check_username):
        user = User.query.filter_by(username=check_username.data).first()
        if user:
            raise ValidationError('Username already exists!')

    def validate_email_address(self, check_email_address):
        mail = User.query.filter_by(email_address=check_email_address.data).first()
        if mail:
            raise ValidationError('Email address already exists!')

    names = StringField(label='Names:', validators=[Length(min=2, max=40), DataRequired()])
    lastname = StringField(label='Last Name:', validators=[Length(min=2, max=30), DataRequired()])
    phone = StringField(label='Phone:', validators=[Length(min=11, max=14), DataRequired()])
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email('Input correct email address.'), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class FoodMenuForm(FlaskForm):
    #look up how to get the present date
    date = StringField(label='Date', validators=[Length(min=2, max=30), DataRequired()])
    brunch = StringField(label='Brunch', validators=[Length(min=2, max=30), DataRequired()])
    dinner = StringField(label='Dinner', validators=[Length(min=2, max=30), DataRequired()])
    update = SubmitField(label='Update')

class ClassesForm(FlaskForm):
    name = StringField(label='Class', validators=[Length(min=1, max=30), DataRequired()])
    location = StringField(label='Location', validators=[Length(min=1, max=30), DataRequired()])
    update_status=SubmitField(label='Update status')
    add_class = SubmitField(label='Add class')
