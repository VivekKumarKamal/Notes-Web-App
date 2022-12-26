from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from os import path

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# In python the convention is to name the class in capital letter
# But in line 10 "user.id"(the green one) is in sql where it is same as U


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100), nullable=True)
    second_name = db.Column(db.String(100), nullable=True)


    notes = db.relationship('Note')


