from flask_login import UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Lesson(db.Model):
    lesson_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    student_id = db.Column(db.String(255), db.ForeignKey('student.student_id'))
    student_name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    time_date = db.Column(db.DateTime, default=datetime.utcnow)
    length = db.Column(db.Float)


class Student(db.Model):
    student_id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    address = db.Column(db.String(255))
    gear = db.Column(db.String(255))
    status = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lessons = db.relationship('Lesson')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    students = db.relationship('Student')
