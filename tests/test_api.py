import unittest
from unittest import mock

import api

from tests.base_db_class_for_tests import InitTestDbForTests

from tests.test_db_settings.settings import test_engine


class TestIndGroup(InitTestDbForTests):
    def setUp(self, students=None, groups=None, courses=None,
              students_courses=None, students_group=None) -> None:
        super().setUp()

        api.app.config['TESTING'] = True

        self.app = api.app.test_client()

    @mock.patch.object(
        api.IndGroup.group_interface, '_engine', new=test_engine
    )
    def test_get_group(self):
        groups_id = [1, 3, 5]
        expected_jsons = [
            {'group_id': 1, 'group_name': 'SD-58'},
            {'group_id': 3, 'group_name': 'DD-30'},
            {'group_id': 5, 'group_name': 'CX-73'}
        ]

        for id_, expected_json in zip(groups_id, expected_jsons):
            received_json = self.app.get(f'/api/v1/groups/{id_}/').get_json()

            with self.subTest():
                self.assertEqual(received_json, expected_json)

    @mock.patch.object(
        api.IndGroup.group_interface, '_engine', new=test_engine
    )
    def test_get_group_with_invalid_id(self):
        invalid_ids = [11, 132, 255]

        for id_ in invalid_ids:
            error_json = {'message': f'Group with given {id_} id'
                                     ' does not exists!'}

            response = self.app.get(f'/api/v1/groups/{id_}/')

            with self.subTest():
                self.assertEqual(response.get_json(), error_json)
                self.assertEqual(response.status_code, 404)


class TestGroups(InitTestDbForTests):
    def setUp(self, students=None, groups=None, courses=None,
              students_courses=None, students_group=None) -> None:
        super().setUp()

        api.app.config['TESTING'] = True

        self.app = api.app.test_client()

    @mock.patch.object(
        api.Groups.group_interface, '_engine', new=test_engine
    )
    def test_get_all_groups(self):
        expected_json = {
            'groups': [
                {'group_id': 1, 'group_name': 'SD-58'},
                {'group_id': 2, 'group_name': 'TU-69'},
                {'group_id': 3, 'group_name': 'DD-30'},
                {'group_id': 4, 'group_name': 'QK-85'},
                {'group_id': 5, 'group_name': 'CX-73'}
            ]
        }

        received_json = self.app.get('/api/v1/groups/').get_json()

        self.assertEqual(received_json, expected_json)

    @mock.patch.object(
        api.Groups.group_interface, '_engine', new=test_engine
    )
    def test_get_all_groups_with_students_count(self):
        students_count_groups = {
            1: {
                'groups': [{'group_id': 5, 'group_name': 'CX-73'}]
            },

            2: {
                'groups': [
                    {'group_id': 2, 'group_name': 'TU-69'},
                    {'group_id': 3, 'group_name': 'DD-30'},
                    {'group_id': 4, 'group_name': 'QK-85'},
                    {'group_id': 5, 'group_name': 'CX-73'},
                ]
            }
        }

        for students_count, expected_groups in students_count_groups.items():
            received_json = self.app.get(
                f'/api/v1/groups/?students_count={students_count}'
            ).get_json()

            with self.subTest():
                self.assertEqual(received_json, expected_groups)

    @mock.patch.object(
        api.Groups.group_interface, '_engine', new=test_engine
    )
    def test_get_not_existing_groups_with_students_count(self):
        not_existing_students_count = [0, -2, -5]

        error_json = {'message': 'There is no information about any group!'}

        for student_count in not_existing_students_count:
            response = self.app.get(
                f'/api/v1/groups/?students_count={student_count}'
            )

            with self.subTest():
                self.assertEqual(response.get_json(), error_json)
                self.assertEqual(response.status_code, 404)


class TestIndStudent(InitTestDbForTests):
    def setUp(self, students=None, groups=None, courses=None,
              students_courses=None, students_group=None) -> None:
        super().setUp()

        api.app.config['TESTING'] = True

        self.app = api.app.test_client()

    @mock.patch.object(
        api.IndStudent.student_interface, '_engine', new=test_engine
    )
    def test_get_student(self):
        student_ids = [1, 5, 7]

        expected_jsons = [
            {
                'student_id': 1, 'first_name': 'Benjamin',
                'last_name': 'Miller', 'group_id': 1
            },

            {
                'student_id': 5, 'first_name': 'Evelyn',
                'last_name': 'White', 'group_id': 2
            },

            {
                'student_id': 7, 'first_name': 'Isabella',
                'last_name': 'Martin', 'group_id': 3
            }
        ]

        for id_, student_json in zip(student_ids, expected_jsons):
            received_json = self.app.get(f'/api/v1/students/{id_}/').get_json()

            with self.subTest():
                self.assertEqual(received_json, student_json)

    @mock.patch.object(
        api.IndStudent.student_interface, '_engine', new=test_engine
    )
    def test_get_student_with_invalid_id(self):
        invalid_ids = [220, 15, 331]

        for id_ in invalid_ids:
            error_json = {'message': f'Student with given id ({id_}) '
                                     'does not exists!'}

            response = self.app.get(f'/api/v1/students/{id_}/')

            with self.subTest():
                self.assertEqual(response.get_json(), error_json)
                self.assertEqual(response.status_code, 404)

    @mock.patch.object(
        api.IndStudent.student_interface, '_engine', new=test_engine
    )
    def test_get_student_courses(self):
        student_ids = [3, 2, 6]

        expected_courses_jsons = [
            {'3': {
                'courses': [
                    {'course_id': 1, 'course_name': 'Geography',
                     'course_description': 'Test description for Geography'},
                    {'course_id': 4, 'course_name': 'Writing',
                     'course_description': 'Test description for Writing'},
                    {'course_id': 5, 'course_name': 'German',
                     'course_description': 'Test description for German'}
                ]
            }},

            {'2': {
                'courses': [
                    {'course_id': 1, 'course_name': 'Geography',
                     'course_description': 'Test description for Geography'}
                ]
            }},

            {'6': {
                'courses': [
                    {'course_id': 4, 'course_name': 'Writing',
                     'course_description': 'Test description for Writing'}
                ]
            }}
        ]

        for id_, student_courses_json in zip(student_ids,
                                             expected_courses_jsons):
            received_json = self.app.get(
                f'/api/v1/students/{id_}/?show_courses=true'
            ).get_json()

            with self.subTest():
                self.assertEqual(received_json, student_courses_json)

    @mock.patch.object(
        api.IndStudent.student_interface, '_engine', new=test_engine
    )
    def test_delete_student(self):
        student_ids = [1, 2, 3]

        for id_ in student_ids:
            expected_confirmation = {'message': f'Student (id: {id_})'
                                                ' was successfully deleted'}

            delete_json = self.app.delete(
                f'/api/v1/students/{id_}/'
            ).get_json()

            error_json = {'message': f'Student with given id ({id_}) '
                                     'does not exists!'}

            get_response = self.app.get(f'/api/v1/students/{id_}/')

            with self.subTest():
                self.assertEqual(delete_json, expected_confirmation)

                self.assertEqual(get_response.get_json(), error_json)
                self.assertEqual(get_response.status_code, 404)

    @mock.patch.object(
        api.IndStudent.student_interface, '_engine', new=test_engine
    )
    def test_delete_student_with_invalid_id(self):
        invalid_ids = [331, 24, 15]

        for id_ in invalid_ids:
            error_json = {'message': f'Student with given id ({id_}) '
                                     'does not exists!'}

            response = self.app.delete(f'/api/v1/students/{id_}/')

            with self.subTest():
                self.assertEqual(response.get_json(), error_json)
                self.assertEqual(response.status_code, 404)

    @mock.patch.object(
        api.IndStudent.student_interface, '_engine', new=test_engine
    )
    def test_delete_student_course(self):
        student_id = 3

        # all of this student's courses.
        courses_to_delete = ['German', 'Geography', 'Writing']

        for course in courses_to_delete:
            expected_confirmation = {'message': f'Student (id: {student_id}) '
                                                'was successfully removed '
                                                f'from course ({course})'}

            response = self.app.delete(
                f'/api/v1/students/{student_id}/?course_name={course}'
            )

            with self.subTest():
                self.assertEqual(response.get_json(), expected_confirmation)

        courses_after_delete = self.app.get(
            f'/api/v1/students/{student_id}/?show_courses=true'
        ).get_json()

        expected_courses = {"3": {'courses': []}}

        self.assertEqual(courses_after_delete, expected_courses)

    @mock.patch.object(
        api.IndStudent.student_interface, '_engine', new=test_engine
    )
    def test_delete_student_course_with_invalid_course_name(self):
        invalid_courses = ('Math', 'English', 'Astronomy')
        student_ids = [1, 7, 9]

        for id_, course in zip(student_ids, invalid_courses):
            error_json = {'message': f'Student (id: {id_}) '
                                     f'does not have given course ({course})!'}

            response = self.app.delete(
                f'api/v1/students/{id_}/?course_name={course}'
            )

            with self.subTest():
                self.assertEqual(response.get_json(), error_json)
                self.assertEqual(response.status_code, 404)

    @mock.patch.object(
        api.IndStudent.student_interface, '_engine', new=test_engine
    )
    def test_post_new_student(self):
        student_ids = [11, 12, 13]

        new_students_data = [
            {'first_name': 'Larry', 'last_name': 'Bottom', 'group_id': 3},
            {'first_name': 'Harry', 'last_name': 'Erland', 'group_id': 2},
            {'first_name': 'Marry', 'last_name': 'Bottom', 'group_id': 1}
        ]

        for id_, student_data in zip(student_ids, new_students_data):
            expected_confirmation = {
                'message': f'Student with given id ({id_}) '
                           'was successfully added'
            }

            response = self.app.post(
                f'/api/v1/students/{id_}/', json=student_data
            )

            expected_student_json = {
                'student_id': id_, 'first_name': student_data['first_name'],
                'last_name': student_data['last_name'],
                'group_id': student_data['group_id']
            }

            new_student_json = self.app.get(
                f'/api/v1/students/{id_}/'
            ).get_json()

            with self.subTest():
                self.assertEqual(response.get_json(), expected_confirmation)

                self.assertEqual(new_student_json, expected_student_json)

    @mock.patch.object(
        api.IndStudent.student_interface, '_engine', new=test_engine
    )
    def test_post_new_student_with_existing_id(self):
        existing_ids = [1, 3, 2]

        test_json = {'first_name': 'Test', 'last_name': 'Test', 'group_id': 3}

        for id_ in existing_ids:
            error_json = {'message': f'Student with given id ({id_}) '
                                     'already exists!'}

            response = self.app.post(
                f'/api/v1/students/{id_}/', json=test_json
            )

            with self.subTest():
                self.assertEqual(response.get_json(), error_json)
                self.assertEqual(response.status_code, 400)

    @mock.patch.object(
        api.IndStudent.student_interface, '_engine', new=test_engine
    )
    def test_post_new_student_with_invalid_requested_json(self):
        student_id = 11

        invalid_json = {'firstName': 'Alex', 'lastName': 'Black',
                        'groupId': '4'}

        error_json = {'message': [{'loc': ['first_name'],
                                   'msg': 'field required',
                                   'type': 'value_error.missing'},
                                  {'loc': ['last_name'],
                                   'msg': 'field required',
                                   'type': 'value_error.missing'},
                                  {'loc': ['group_id'],
                                   'msg': 'field required',
                                   'type': 'value_error.missing'}]
                      }

        response = self.app.post(
            f'/api/v1/students/{student_id}/', json=invalid_json
        )

        self.assertEqual(response.get_json(), error_json)
        self.assertEqual(response.status_code, 400)

    @mock.patch.object(
        api.IndStudent.student_interface, '_engine', new=test_engine
    )
    @mock.patch.object(
        api.IndGroup.group_interface, '_engine', new=test_engine
    )
    def test_post_new_student_with_incorrect_group_id_in_requested_json(self):
        student_ids = [11, 12, 13]

        new_students_data = [
            {'first_name': 'Larry', 'last_name': 'Bottom', 'group_id': 11},
            {'first_name': 'Harry', 'last_name': 'Erland', 'group_id': 15},
            {'first_name': 'Marry', 'last_name': 'Bottom', 'group_id': 21}
        ]

        for id_, student_data in zip(student_ids, new_students_data):
            error_json = {'message': f'Group with given id '
                                     f'({student_data["group_id"]}) '
                                     'does not exists!'}

            response = self.app.post(
                f'/api/v1/students/{id_}/', json=student_data
            )

            with self.subTest():
                self.assertEqual(response.get_json(), error_json)
                self.assertEqual(response.status_code, 404)

    @mock.patch.object(
        api.IndStudent.student_interface, '_engine', new=test_engine
    )
    def test_post_student_course(self):
        student_id = 6
        courses_to_add = ['Computer studies', 'Geography']

        for course in courses_to_add:
            expected_confirmation = {
                'message': f'Student (id: {student_id}) successfully'
                           f' added to the course ({course})'
            }

            response = self.app.post(
                f'/api/v1/students/{student_id}/?course_name={course}'
            )

            with self.subTest():
                self.assertEqual(response.get_json(), expected_confirmation)

        student_courses = self.app.get(
            f'/api/v1/students/{student_id}/?show_courses=true'
        ).get_json()

        student_courses = [
            course['course_name'] for course in
            student_courses[str(student_id)]['courses']
        ]

        self.assertTrue(set(courses_to_add).issubset(set(student_courses)))

    @mock.patch.object(
        api.IndStudent.student_interface, '_engine', new=test_engine
    )
    def test_post_student_not_existing_course(self):
        student_id = 1
        not_existing_courses = ('Math', 'English', 'Astronomy')

        for course in not_existing_courses:
            error_json = {'message': f'Course with given name ({course}) '
                                     'does not exists!'}

            response = self.app.post(
                f'/api/v1/students/{student_id}/?course_name={course}'
            )

            with self.subTest():
                self.assertEqual(response.get_json(), error_json)
                self.assertEqual(response.status_code, 400)


class TestStudents(InitTestDbForTests):
    def setUp(self, students=None, groups=None, courses=None,
              students_courses=None, students_group=None) -> None:
        super().setUp()

        api.app.config['TESTING'] = True

        self.app = api.app.test_client()

    @mock.patch.object(
        api.Students.student_interface, '_engine', new=test_engine
    )
    def test_get_all_students(self):
        expected_json = {
            'students': [
                {'student_id': 1, 'first_name': 'Benjamin',
                 'last_name': 'Miller', 'group_id': 1},

                {'student_id': 2, 'first_name': 'Alexander',
                 'last_name': 'Johnson', 'group_id': 1},

                {'student_id': 3, 'first_name': 'Mia', 'last_name': 'Wilson',
                 'group_id': 1},

                {'student_id': 4, 'first_name': 'Charlotte',
                 'last_name': 'Brown', 'group_id': 2},

                {'student_id': 5, 'first_name': 'Evelyn', 'last_name': 'White',
                 'group_id': 2},

                {'student_id': 6, 'first_name': 'Olivia', 'last_name': 'White',
                 'group_id': 3},

                {'student_id': 7, 'first_name': 'Isabella',
                 'last_name': 'Martin', 'group_id': 3},

                {'student_id': 8, 'first_name': 'Mia', 'last_name': 'Thompson',
                 'group_id': 4},

                {'student_id': 9, 'first_name': 'Ava', 'last_name': 'Thompson',
                 'group_id': 4},

                {'student_id': 10, 'first_name': 'Lucas', 'last_name': 'Jones',
                 'group_id': 5}
            ]
        }

        received_json = self.app.get(
            '/api/v1/students/'
        ).get_json()

        self.assertEqual(received_json, expected_json)

    @mock.patch.object(
        api.Students.student_interface, '_engine', new=test_engine
    )
    def test_get_all_students_related_to_group(self):
        courses = ['Geography', 'Art']

        expected_jsons = [
            {'students': [
                {'student_id': 1, 'first_name': 'Benjamin',
                 'last_name': 'Miller', 'group_id': 1},

                {'student_id': 2, 'first_name': 'Alexander',
                 'last_name': 'Johnson', 'group_id': 1},

                {'student_id': 3, 'first_name': 'Mia', 'last_name': 'Wilson',
                 'group_id': 1},

                {'student_id': 8, 'first_name': 'Mia', 'last_name': 'Thompson',
                 'group_id': 4}
            ]},

            {'students': [
                {'student_id': 1, 'first_name': 'Benjamin',
                 'last_name': 'Miller', 'group_id': 1},

                {'student_id': 4, 'first_name': 'Charlotte',
                 'last_name': 'Brown', 'group_id': 2},

                {'student_id': 5, 'first_name': 'Evelyn', 'last_name': 'White',
                 'group_id': 2},

                {'student_id': 9, 'first_name': 'Ava', 'last_name': 'Thompson',
                 'group_id': 4},

                {'student_id': 10, 'first_name': 'Lucas', 'last_name': 'Jones',
                 'group_id': 5}
            ]}
        ]

        for course, students_json in zip(courses, expected_jsons):
            received_json = self.app.get(
                f'/api/v1/students/?course_name={course}'
            ).get_json()

            with self.subTest():
                self.assertEqual(received_json, students_json)

    @mock.patch.object(
        api.Students.student_interface, '_engine', new=test_engine
    )
    def test_get_all_students_related_to_invalid_course(self):
        invalid_courses = ('Math', 'English', 'Astronomy')

        error_json = {"message": "There is no information about any student!"}

        for course in invalid_courses:
            response = self.app.get(
                f'/api/v1/students/?course_name={course}'
            )

            with self.subTest():
                self.assertEqual(response.get_json(), error_json)
                self.assertEqual(response.status_code, 404)


class TestIndCourse(InitTestDbForTests):
    def setUp(self, students=None, groups=None, courses=None,
              students_courses=None, students_group=None) -> None:
        super().setUp()

        api.app.config['TESTING'] = True

        self.app = api.app.test_client()

    @mock.patch.object(
        api.IndCourse.course_interface, '_engine', new=test_engine
    )
    def test_get_course(self):
        course_ids = [1, 2, 5]

        expected_jsons = [
            {'course_id': 1, 'course_name': 'Geography',
             'course_description': 'Test description for Geography'},

            {'course_id': 2, 'course_name': 'Art',
             'course_description': 'Test description for Art'},

            {'course_id': 5, 'course_name': 'German',
             'course_description': 'Test description for German'}
        ]

        for id_, course_json in zip(course_ids, expected_jsons):
            received_json = self.app.get(f'/api/v1/courses/{id_}/').get_json()

            with self.subTest():
                self.assertEqual(received_json, course_json)

    @mock.patch.object(
        api.IndCourse.course_interface, '_engine', new=test_engine
    )
    def test_get_course_with_invalid_id(self):
        invalid_course_id = [20, 30, 40]

        for id_ in invalid_course_id:
            error_json = {'message': f'Course with given id ({id_}) '
                                     ' does not exists!'}

            response = self.app.get(
                f'/api/v1/courses/{id_}/'
            )

            with self.subTest():
                self.assertEqual(response.get_json(), error_json)
                self.assertEqual(response.status_code, 404)


class TestCourses(InitTestDbForTests):
    def setUp(self, students=None, groups=None, courses=None,
              students_courses=None, students_group=None) -> None:
        super().setUp()

        api.app.config['TESTING'] = True

        self.app = api.app.test_client()

    @mock.patch.object(
        api.Courses.course_interface, '_engine', new=test_engine
    )
    def test_get_all_courses(self):
        expected_json = {'courses': [
            {'course_id': 1, 'course_name': 'Geography',
             'course_description': 'Test description for Geography'},
            {'course_id': 2, 'course_name': 'Art',
             'course_description': 'Test description for Art'},
            {'course_id': 3, 'course_name': 'Computer studies',
             'course_description': 'Test description for Computer studies'},
            {'course_id': 4, 'course_name': 'Writing',
             'course_description': 'Test description for Writing'},
            {'course_id': 5, 'course_name': 'German',
             'course_description': 'Test description for German'}
        ]}

        received_json = self.app.get(
            '/api/v1/courses/'
        ).get_json()

        self.assertEqual(received_json, expected_json)


if __name__ == '__main__':
    unittest.main()
