from flask import render_template, abort

from app import app

from models.manage_school_db import CourseInterface
from models.manage_school_db import StudentInterface
from models.manage_school_db import GroupInterface


student_interface = StudentInterface()
group_interface = GroupInterface()
course_interface = CourseInterface()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/groups/')
def show_groups():
    if not (groups := group_interface.get_all_groups()):
        abort(404)

    return render_template('groups.html', groups=groups)


@app.route('/groups/<int:group_id>')
def show_group(group_id: int):
    if not (group := group_interface.get_group_by_id(group_id)):
        abort(404)

    return render_template('group_detail.html', group=group)


@app.route('/groups/<int:group_id>/students')
def show_students_related_to_group(group_id):
    students = student_interface.get_students_related_to_group(group_id)

    if not students:
        abort(404)

    return render_template('students.html', students=students)


@app.route('/students/')
def show_students():
    if not (students := student_interface.get_all_students()):
        abort(404)

    return render_template('students.html', students=students)


@app.route('/students/<int:student_id>')
def show_student(student_id: int):
    if not (
            student := student_interface.get_student_with_full_info(student_id)
    ):
        abort(404)

    return render_template('student_detail.html', student=student)


@app.route('/courses/')
def show_courses():
    if not (courses := course_interface.get_all_courses()):
        abort(404)

    return render_template('courses.html', courses=courses)


@app.route('/courses/<int:course_id>')
def show_course(course_id: int):
    if not (course := course_interface.get_course_by_id(course_id)):
        abort(404)

    return render_template('course_detail.html', course=course)


@app.route('/courses/<int:course_id>/students')
def show_students_related_to_course(course_id):
    if not (course := course_interface.get_course_by_id(course_id)):
        abort(404)

    students = student_interface.get_students_related_to_course(course.name)

    if not students:
        abort(404)

    return render_template('students.html', students=students)
