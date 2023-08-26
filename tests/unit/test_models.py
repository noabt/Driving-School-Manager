from helpers.models import User, Student, Lesson
from werkzeug.security import generate_password_hash, check_password_hash

def test_new_user():
  user = User(username='testusername', first_name='testname', password=generate_password_hash('testpassword', method='sha256'))
  assert user.username == 'testusername'
  assert user.first_name == 'testname'
  assert user.password != 'testpassword'

def test_new_student():
  student = Student(student_id='123456789', name='name', phone='phone', address='address', gear='gear', status='status', user_id='2')  
  assert student.student_id == '123456789'
  assert student.name == 'name'
  assert student.phone == 'phone'
  assert student.address == 'address'
  assert student.gear == 'gear'
  assert student.status == 'status'
  assert student.user_id == '2'

def test_new_lesson():
  lesson = Lesson(user_id='2', student_id='123456789', student_name='name', address='address', time_date='2023-08-26 14:30:00', length='1.5')  
  assert lesson.student_id == '123456789'
  assert lesson.student_name == 'name'
  assert lesson.time_date == '2023-08-26 14:30:00'
  assert lesson.address == 'address'
  assert lesson.length == '1.5'
  assert lesson.user_id == '2'


