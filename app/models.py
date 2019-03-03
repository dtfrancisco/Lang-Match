from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    answers = db.relationship('Answer', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


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
