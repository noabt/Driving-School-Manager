import datetime
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
import json
from .models import Student, Lesson
from datetime import date, datetime
from sqlalchemy import extract


today_date=datetime.date

views = Blueprint('views', __name__)


@views.route("/", methods=['get'])
@login_required
def home():
    today = Lesson.query.filter(extract('month', Lesson.time_date) == datetime.today().month,
                         extract('year', Lesson.time_date) == datetime.today().year,
                         extract('day', Lesson.time_date) == datetime.today().day).order_by(Lesson.time_date).all()
    rows = Student.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, rows=rows, today=today)

@views.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student_id = request.form.get('id')
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        gear = request.form.get('gear')
        status = request.form.get('status')

        existing_student = Student.query.filter_by(student_id=student_id).first()

        if len(student_id) != 9:
            flash('id is too short!', category='error')
            rows = Student.query.filter_by(user_id=current_user.id).all()
            return render_template("home.html", user=current_user, rows=rows)
        elif len(name) < 2:
            flash('name is too short!', category='error')
            rows = Student.query.filter_by(user_id=current_user.id).all()
            return render_template("home.html", user=current_user, rows=rows)
        elif len(phone) != 10:
            flash('phone number is too short!', category='error')
            rows = Student.query.filter_by(user_id=current_user.id).all()
            return render_template("home.html", user=current_user, rows=rows)
        elif existing_student:
            flash('Student ID already exists or is registered for another teacher', category='success')
            rows = Student.query.filter_by(user_id=current_user.id).all()
            return render_template("home.html", user=current_user, rows=rows)
        else:
            new_student = Student(student_id=student_id, name=name, phone=phone, address=address, gear=gear, status=status, user_id=current_user.id)  #providing the schema for the note
            db.session.add(new_student) #adding the student to the database
            db.session.commit()
            rows = Student.query.filter_by(user_id=current_user.id).all()
            flash('Student added!', category='success')
            return render_template("home.html", user=current_user, rows=rows)

    return render_template("home.html", user=current_user)

@views.route('/update', methods=['GET', 'POST'])
def update_student():
    if request.method == 'POST':
        data = Student.query.get(request.form.get('id'))
        data.student_id = request.form.get('student_id')
        data.name = request.form.get('name')
        data.phone = request.form.get('phone')
        data.address = request.form.get('address')
        data.gear = request.form.get('gear')
        data.status = request.form.get('status')

        db.session.commit()
        rows = Student.query.filter_by(user_id=current_user.id).all()
        flash('Student Updated!', category='success')
        return render_template("home.html", user=current_user, rows=rows)

    return render_template("home.html", user=current_user)


@views.route('/delete/<student_id>/', methods=['GET', 'POST'])
def delete_student(student_id):
    data = Student.query.get(student_id)
    db.session.delete(data)
    db.session.commit()
    rows = Student.query.filter_by(user_id=current_user.id).all()
    flash('Student deleted!', category='success')
    return render_template("home.html", user=current_user, rows=rows)


@views.route("/homePage/searchById", methods=["POST"])
def searchS_By_Id():
    student_id = request.form['search-id']
    existing_student = Student.query.filter_by(student_id=student_id).first()
    if existing_student:
        rows = Student.query.filter_by(student_id=student_id).all()
        return render_template("home.html", user=current_user, rows=rows)
    else:
        flash('No student matching this ID was found!', category='error')
        rows = Student.query.filter_by(user_id=current_user.id).all()
        return render_template("home.html", user=current_user, rows=rows)

@views.route("/homePage/searchByName", methods=["POST"])
def searchS_By_Name():
    name = request.form['search-name']
    existing_student = Student.query.filter_by(name=name, user_id=current_user.id).first()
    if existing_student:
        rows = Student.query.filter_by(name=name, user_id=current_user.id).all()
        return render_template("home.html", user=current_user, rows=rows)
    else:
        flash('No student matching this name was found!', category='error')
        rows = Student.query.filter_by(user_id=current_user.id).all()
        return render_template("home.html", user=current_user, rows=rows)

@views.route("/todayLessons", methods=["GET"])
def today_lesson():
    pass

##############################################################################
#Lesson related routing
##############################################################################
@views.route("/lessons/<student_id>", methods=['GET', 'POST'])
def Lesson_list(student_id):
    student = Student.query.get(student_id)
    lessons = Lesson.query.filter_by(student_id=student_id).all()
    return render_template("lessons.html", user=current_user, student=student, lessons=lessons)

@views.route("/lessons/addLesson/<student_id>", methods=['GET', 'POST'])
def add_lesson(student_id):
    student = Student.query.get(student_id)
    if request.method == 'POST':
        student_id = student.student_id
        student_name = student.name
        time_date = request.form.get('timedate')
        address = student.address
        length = request.form.get('length')

        existing_lesson = Lesson.query.filter_by(time_date=time_date).first()

        if existing_lesson:
            flash('There is already a lesson at that time and date', category='error')
            lessons = Lesson.query.filter_by(student_id=student.student_id).all()
            return render_template("lessons.html", user=current_user, student=student, lessons=lessons)
        else:
            new_lesson = Lesson(user_id=current_user.id, student_id=student_id, student_name=student_name, address=address, time_date=time_date, length=length)  #providing the schema for the lesson
            db.session.add(new_lesson) #adding the lesson to the database
            db.session.commit()
            lessons = Lesson.query.filter_by(student_id=student.student_id).all()
            flash('Lesson added!', category='success')
            return render_template("lessons.html", user=current_user, student=student, lessons=lessons)

    lessons = Lesson.query.filter_by(student_id=student.student_id).all()
    return render_template("lessons.html", user=current_user, student=student, lessons=lessons)

@views.route("/lessons/searchByDate", methods=['GET', 'POST'])
def searchL_By_Date():
    pass

@views.route("/updateLesson", methods=['GET', 'POST'])
def update_lesson():
    if request.method == 'POST':
        student = Student.query.get(request.form.get('student_id'))
        lesson = Lesson.query.get(request.form.get('id'))
        lesson.student_id = student.student_id
        lesson.student_name = student.name
        lesson.address = request.form.get('address')
        lesson.time_date = request.form.get('timedate')
        lesson.length = request.form.get('length')
        db.session.commit()
        lessons = Lesson.query.filter_by(student_id=request.form.get('student_id')).all()
        flash('Student Updated!', category='success')
        return render_template("lessons.html", user=current_user, lessons=lessons, student=student)

    return render_template("lessons.html", user=current_user)


@views.route("/delete/<student_id>/<lesson_id>", methods=['GET', 'POST'])
def delete_lesson(lesson_id, student_id):
    student = Student.query.get(student_id)
    data = Lesson.query.get(lesson_id)
    db.session.delete(data)
    db.session.commit()
    lessons = Lesson.query.filter_by(student_id=student.student_id).all()
    flash('Lesson deleted!', category='success')
    return render_template("lessons.html", user=current_user, student=student, lessons=lessons)