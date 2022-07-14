from datetime import date
from email.policy import default
from flask_login import UserMixin
from decalog import db, login_manager
from decalog import bcrypt

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    names = db.Column(db.String(length=30), nullable=False)
    lastname = db.Column(db.String(length=30), nullable=False)
    phone = db.Column(db.String(), nullable=False)
    stack = db.Column(db.String(), nullable=True)
    room_number = db.Column(db.Integer())
    status = db.Column(db.String(length=30), default='Available')
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)

    def __repr__(self):
        return f'User {self.username}'

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class FoodMenu(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.String(length=30), nullable=False)
    brunch = db.Column(db.String(length=30), nullable=False)
    dinner = db.Column(db.String(length=25), nullable=False)

class Classes(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    location = db.Column(db.String(length=30), nullable=False)
    class_status = db.Column(db.String(length=30), default='Available')
    color = db.Column(db.String(length=30), default='green')

class Log(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    day = db.Column(db.String(length=30), nullable=False)
    date = db.Column(db.String(length=30), nullable=False)
    names = db.Column(db.String(length=30), nullable=True)
    lastname = db.Column(db.String(length=30), nullable=True)
    user_id = db.Column(db.Integer())
    signout_time = db.Column(db.String(length=20), nullable=True)
    signin_time = db.Column(db.String(length=20), nullable=True)