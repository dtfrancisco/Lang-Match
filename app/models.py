from flask_login import UserMixin
from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
import requests
from io import BytesIO


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), index=True, unique=True)
    password_hash = db.Column(db.String(40))
    email = db.Column(db.String(80), index=True, unique=True)
    gender = db.Column(db.String(6))
    birthday = db.Column(db.Date)
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(5))
    privacy = db.Column(db.String(20))  # Hide profile from non-users
    answers = db.relationship('Answer', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        r = requests.get("http://www.blankinshippt.com/images/icons/blank-person.jpg")
        img = Image.open(BytesIO(r.content))
        new_width, new_height = size, size
        img.resize((new_width, new_height), Image.ANTIALIAS)
        return img

    def __repr__(self):
        return '<User {}>'.format(self.username)

# Load a user from the database given an id


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140), unique=True)
    type = db.Column(db.String(20), index=True)  # summary vs. short answer
    answers = db.relationship('Answer', backref='question', lazy='dynamic')

    def __repr__(self):
        return '<Question {}>'.format(self.body)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    def __repr__(self):
        return '<Answer {}>'.format(self.body)
