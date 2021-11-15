from typing import List, Type

import json

from flask_restful import Api, Resource, abort, reqparse

from flask import request

from flasgger import swag_from, Swagger

from app import app

from models.manage_school_db import CourseInterface
from models.manage_school_db import StudentInterface
from models.manage_school_db import GroupInterface
from models.manage_school_db import Student, Group, Course

from schemas.json_schemas import StudentSchema, ValidationError


api = Api(app)
swagger = Swagger(app)

parser = reqparse.RequestParser()
parser.add_argument('students_count', type=int, location='args')
parser.add_argument('course_name', type=str, location='args')
parser.add_argument('show_courses', type=str, location='args')


class IndGroup(Resource):
    group_interface = GroupInterface()

    @classmethod
    def build_json_response(cls, group: Group) -> dict:
        response = {
            'group_id': group.id, 'group_name': group.name,
        }

        return response

    @classmethod
    def get_group_or_abort(cls, group_id: int) -> Group:
        if not (group := cls.group_interface.get_group_by_id(group_id)):
            abort(404, message=f'Group with given {group_id} id'
                               ' does not exists!')
        return group

    @classmethod
    def abort_if_group_not_exists(cls, group_id: int):
        if not cls.group_interface.check_if_group_exists(group_id):
            abort(404, message=f'Group with given id ({group_id}) '
                               'does not exists!')

    @classmethod
    @swag_from('yaml_for_swagger/groupGet.yaml')
    def get(cls, group_id: int) -> dict:
        group = cls.get_group_or_abort(group_id)
        return cls.build_json_response(group)


class Groups(Resource):
    group_interface = GroupInterface()

    @classmethod
    def build_json_response(cls, groups: List[Group]) -> dict:
        response = {'groups': []}

        for group in groups:
            response['groups'].append(
                IndGroup.build_json_response(group.Group)
            )

        return response

    @classmethod
    def get_groups_or_abort(cls, students_count=None) -> List[Group]:
        if students_count or students_count == 0:
            groups = cls.group_interface.get_group_with_less_students_count(
                    students_count
                )

        else:
            groups = cls.group_interface.get_all_groups()

        if not groups:
            abort(404, message='There is no information about any group!')

        return groups

    @classmethod
    @swag_from('yaml_for_swagger/groupsGet.yaml')
    def get(cls) -> dict:
        args = parser.parse_args()
        students_count = args.students_count

        groups = cls.get_groups_or_abort(students_count)

        return cls.build_json_response(groups)


class IndStudent(Resource):
    student_interface = StudentInterface()

    @classmethod
    def build_json_response(cls, student: Student) -> dict:
        response = {
            'student_id': student.id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'group_id': student.group_id
        }

        return response

    @classmethod
    def get_student_or_abort(cls, student_id: int) -> Student:
        if not (
                student := cls.student_interface.get_student_by_id(student_id)
        ):
            abort(404, message=f'Student with given id ({student_id}) '
                               'does not exists!')
        return student

    @classmethod
    def build_json_student_courses_response(cls, student_id: int):
        cls.abort_if_student_not_exists(student_id)

        student = cls.student_interface.get_student_with_full_info(student_id)
        student_courses = student.courses

        json_response = {
            student_id: {'courses': []}
        }

        for course in student_courses:
            json_response[student_id]['courses'].append(
                IndCourse.build_json_response(course)
            )

        return json_response

    @classmethod
    @swag_from('yaml_for_swagger/studentGet.yaml')
    def get(cls, student_id: int) -> dict:
        args = parser.parse_args()
        show_courses = args.show_courses

        if show_courses == 'true':
            return cls.build_json_student_courses_response(student_id)

        student = cls.get_student_or_abort(student_id)

        return cls.build_json_response(student)

    @classmethod
    def delete_student(cls, student_id: int) -> dict:
        cls.student_interface.delete_student_by_id(student_id)

        return {'message': f'Student (id: {student_id})'
                           ' was successfully deleted'}

    @classmethod
    def delete_student_from_course(
            cls, student_id: int, course_name: str) -> dict:
        try:
            cls.student_interface.remove_student_from_course(
                student_id, course_name
            )
        except ValueError:
            abort(404, message=f'Student (id: {student_id}) '
                               f'does not have given course ({course_name})!')

        return {'message': f'Student (id: {student_id}) '
                           'was successfully removed '
                           f'from course ({course_name})'}

    @classmethod
    @swag_from('yaml_for_swagger/studentDelete.yaml')
    def delete(cls, student_id: int) -> dict:
        args = parser.parse_args()
        course_name = args.course_name

        cls.abort_if_student_not_exists(student_id)

        if course_name:
            return cls.delete_student_from_course(student_id, course_name)

        return cls.delete_student(student_id)

    @classmethod
    def abort_if_student_already_exists(cls, student_id: int) -> None:
        if cls.student_interface.check_if_student_exists(student_id):
            abort(400, message=f'Student with given id ({student_id}) '
                               'already exists!')

    @classmethod
    def abort_if_student_not_exists(cls, student_id: int) -> None:
        if not cls.student_interface.check_if_student_exists(student_id):
            abort(404, message=f'Student with given id ({student_id}) '
                               'does not exists!')

    @classmethod
    def validate_json_or_abort(
            cls, user_json: dict,
            schema: Type[StudentSchema]) -> StudentSchema:
        student_to_save = None

        try:
            student_to_save = schema.parse_obj(user_json)
        except ValidationError as err:
            abort(400, message=json.loads(err.json()))

        return student_to_save

    @classmethod
    def save_user_or_abort(cls, student_id: int) -> None:
        cls.abort_if_student_already_exists(student_id)

        new_student = cls.validate_json_or_abort(
            request.json, StudentSchema
        )

        IndGroup.abort_if_group_not_exists(new_student.group_id)

        cls.student_interface.add_new_student(
            student_id, new_student.group_id,
            new_student.first_name, new_student.last_name
        )

    @classmethod
    def add_student_to_course_or_abort(
            cls, student_id: int, course_name: str) -> None:
        cls.abort_if_student_not_exists(student_id)

        try:
            cls.student_interface.add_student_to_course(
                student_id, course_name
            )
        except ValueError:
            abort(400, message=f'Course with given name ({course_name}) '
                               'does not exists!')

    @classmethod
    @swag_from('yaml_for_swagger/studentPost.yaml')
    def post(cls, student_id: int):
        args = parser.parse_args()
        course_name = args.course_name

        if course_name:
            cls.add_student_to_course_or_abort(student_id, course_name)

            return {'message': f'Student (id: {student_id}) successfully'
                               f' added to the course ({course_name})'}

        cls.save_user_or_abort(student_id)

        return {'message': f'Student with given id ({student_id}) '
                           'was successfully added'}


class Students(Resource):
    student_interface = StudentInterface()

    @classmethod
    def build_json_response(cls, students: List[Student]) -> dict:
        response = {'students': []}

        for student in students:
            response['students'].append(
                IndStudent.build_json_response(student.Student)
            )

        return response

    @classmethod
    def get_students_or_abort(cls, course_name=None) -> List[Student]:
        if course_name:
            students = cls.student_interface.get_students_related_to_course(
                course_name
            )
        else:
            students = cls.student_interface.get_all_students()

        if not students:
            abort(404, message='There is no information about any student!')

        return students

    @classmethod
    @swag_from('yaml_for_swagger/studentsGet.yaml')
    def get(cls) -> dict:
        args = parser.parse_args()
        course_name = args.course_name

        students = cls.get_students_or_abort(course_name)

        return cls.build_json_response(students)


class IndCourse(Resource):
    course_interface = CourseInterface()

    @classmethod
    def get_course_or_abort(cls, course_id: int) -> Course:
        if not (course := cls.course_interface.get_course_by_id(course_id)):
            abort(404, message=f'Course with given id ({course_id}) '
                               ' does not exists!')
        return course

    @classmethod
    def build_json_response(cls, course: Course) -> dict:
        response = {
            'course_id': course.id,
            'course_name': course.name,
            'course_description': course.description
            }

        return response

    @classmethod
    @swag_from('yaml_for_swagger/courseGet.yaml')
    def get(cls, course_id) -> dict:
        course = cls.get_course_or_abort(course_id)

        return cls.build_json_response(course)


class Courses(Resource):
    course_interface = CourseInterface()

    @classmethod
    def get_courses_or_abort(cls) -> List[Course]:
        if not (courses := cls.course_interface.get_all_courses()):
            abort(404, message='There is no information about any course!')
        return courses

    @classmethod
    def build_json_response(cls, courses: List[Course]) -> dict:
        response = {'courses': []}

        for course in courses:
            course = course.Course

            response['courses'].append(
                IndCourse.build_json_response(course)
            )

        return response

    @classmethod
    @swag_from('yaml_for_swagger/coursesGet.yaml')
    def get(cls) -> dict:
        courses = cls.get_courses_or_abort()

        return cls.build_json_response(courses)


api.add_resource(Groups, '/api/v1/groups/')
api.add_resource(IndGroup, '/api/v1/groups/<int:group_id>/')

api.add_resource(Courses, '/api/v1/courses/')
api.add_resource(IndCourse, '/api/v1/courses/<int:course_id>/')

api.add_resource(Students, '/api/v1/students/')
api.add_resource(IndStudent, '/api/v1/students/<int:student_id>/')
