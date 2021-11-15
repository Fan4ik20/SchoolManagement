import unittest

from models.manage_school_db import StudentInterface, CourseInterface
from models.manage_school_db import GroupInterface

from tests.test_db_settings.settings import test_engine

from tests.base_db_class_for_tests import InitTestDbForTests


class TestStudentInterface(InitTestDbForTests):
    student_interface = StudentInterface(engine=test_engine)

    test_student_data = {
        1: 'Student id: 1 - Benjamin Miller, Group id: 1',
        2: 'Student id: 2 - Alexander Johnson, Group id: 1',
        3: 'Student id: 3 - Mia Wilson, Group id: 1',
        4: 'Student id: 4 - Charlotte Brown, Group id: 2',
        5: 'Student id: 5 - Evelyn White, Group id: 2',
        6: 'Student id: 6 - Olivia White, Group id: 3',
        7: 'Student id: 7 - Isabella Martin, Group id: 3',
        8: 'Student id: 8 - Mia Thompson, Group id: 4',
        9: 'Student id: 9 - Ava Thompson, Group id: 4',
        10: 'Student id: 10 - Lucas Jones, Group id: 5'
    }

    test_student_group = {
        1: "Group id: 1, name: 'SD-58'",
        2: "Group id: 1, name: 'SD-58'",
        3: "Group id: 1, name: 'SD-58'",
        4: "Group id: 2, name: 'TU-69'",
        5: "Group id: 2, name: 'TU-69'",
        6: "Group id: 3, name: 'DD-30'",
        7: "Group id: 3, name: 'DD-30'",
        8: "Group id: 4, name: 'QK-85'",
        9: "Group id: 4, name: 'QK-85'",
        10: "Group id: 5, name: 'CX-73'"
    }

    test_student_courses = {
        1: ["Subject id: 1, name: 'Geography', "
            "description: 'Test description for Geography'",

            "Subject id: 2, name: 'Art', "
            "description: 'Test description for Art'",

            "Subject id: 3, name: 'Computer studies', "
            "description: 'Test description for Computer studies'"],

        2: ["Subject id: 1, name: 'Geography', "
            "description: 'Test description for Geography'"],

        3: ["Subject id: 1, name: 'Geography', "
            "description: 'Test description for Geography'",

            "Subject id: 4, name: 'Writing', "
            "description: 'Test description for Writing'",

            "Subject id: 5, name: 'German', description: "
            "'Test description for German'"],

        4: ["Subject id: 2, name: 'Art', "
            "description: 'Test description for Art'"],

        5: ["Subject id: 2, name: 'Art', "
            "description: 'Test description for Art'",

            "Subject id: 5, name: 'German', "
            "description: 'Test description for German'"],

        6: ["Subject id: 4, name: 'Writing', "
            "description: 'Test description for Writing'"],

        7: ["Subject id: 4, name: 'Writing', "
            "description: 'Test description for Writing'"],

        8: ["Subject id: 1, name: 'Geography', "
            "description: 'Test description for Geography'",

            "Subject id: 3, name: 'Computer studies', "
            "description: 'Test description for Computer studies'",

            "Subject id: 5, name: 'German', "
            "description: 'Test description for German'"],

        9: ["Subject id: 2, name: 'Art', "
            "description: 'Test description for Art'",

            "Subject id: 4, name: 'Writing', "
            "description: 'Test description for Writing'",

            "Subject id: 5, name: 'German', "
            "description: 'Test description for German'"],

        10: ["Subject id: 2, name: 'Art', "
             "description: 'Test description for Art'",

             "Subject id: 3, name: 'Computer studies', "
             "description: 'Test description for Computer studies'",

             "Subject id: 5, name: 'German', "
             "description: 'Test description for German'"]
    }

    not_existing_id = [15, 221, 331, 22]
    not_existing_courses = ['Math', 'English', 'C++']

    def test_get_all_students(self):
        students = self.student_interface.get_all_students()

        # We will check the text representation of object.
        for student, expected_data_ in zip(students,
                                           self.test_student_data.values()):
            student_repr = str(student.Student)

            with self.subTest():
                self.assertEqual(student_repr, expected_data_)

    def test_student_by_id(self):
        for id_, expected_data in self.test_student_data.items():
            student = self.student_interface.get_student_by_id(id_)
            student_repr = str(student)

            with self.subTest():
                self.assertEqual(student_repr, expected_data)

    def test_student_with_not_existing_id(self):
        for id_ in self.not_existing_id:
            student = self.student_interface.get_student_by_id(id_)

            with self.subTest():
                self.assertIsNone(student)

    def test_students_related_to_course(self):
        test_course_student = {
            'Geography': [
                self.test_student_data[1], self.test_student_data[2],
                self.test_student_data[3], self.test_student_data[8]
            ],
            'Art': [
                self.test_student_data[1], self.test_student_data[4],
                self.test_student_data[5], self.test_student_data[9],
                self.test_student_data[10]
            ]
        }

        for course, expected_students in test_course_student.items():
            students = self.student_interface.get_students_related_to_course(
                course)

            for student, expected_data in zip(students, expected_students):
                student_repr = str(student.Student)

                with self.subTest():
                    self.assertEqual(student_repr, expected_data)

    def test_students_related_with_not_existing_course(self):
        for course in self.not_existing_courses:
            student = self.student_interface.get_students_related_to_course(
                course)

            with self.subTest():
                self.assertIsNone(student)

    def test_get_student_with_full_info(self):
        test_id = [7, 5, 2, 1, 3, 4]

        for id_ in test_id:
            student = self.student_interface.get_student_with_full_info(id_)

            with self.subTest():
                student_repr = str(student)
                group_repr = str(student.group)

                self.assertEqual(student_repr, self.test_student_data[id_])
                self.assertEqual(group_repr, self.test_student_group[id_])

                for course, expected_course in zip(
                        student.courses, self.test_student_courses[id_]
                ):
                    course_repr = str(course)

                    with self.subTest():
                        self.assertEqual(course_repr, expected_course)

    def test_get_student_full_info_with_not_existing_id(self):
        for id_ in self.not_existing_id:
            student = self.student_interface.get_student_with_full_info(id_)

            with self.subTest():
                self.assertIsNone(student)

    def test_check_student_exists(self):
        for id_ in self.test_student_data:
            result = self.student_interface.check_if_student_exists(id_)

            with self.subTest():
                self.assertTrue(result)

    def test_check_student_exists_with_not_existing_id(self):
        for id_ in self.not_existing_id:
            result = self.student_interface.check_if_student_exists(id_)

            with self.subTest():
                self.assertFalse(result)

    def test_delete_student_by_id(self):
        for id_ in self.test_student_data:
            self.student_interface.delete_student_by_id(id_)

            result = self.student_interface.check_if_student_exists(id_)

            with self.subTest():
                self.assertEqual(result, False)

    def test_delete_student_by_id_with_not_existing_id(self):
        for id_ in self.not_existing_id:
            with self.subTest():
                with self.assertRaises(ValueError):
                    self.student_interface.delete_student_by_id(id_)

    def test_get_students_related_to_group(self):
        groups_students_id = {
            1: [1, 2, 3], 2: [4, 5], 3: [6, 7], 4: [8, 9], 5: [10]
        }

        for group_id, expected_students_id in groups_students_id.items():
            students = self.student_interface.get_students_related_to_group(
                group_id
            )

            for student, expected_id in zip(
                    students, expected_students_id
            ):
                student_repr = str(student.Student)
                expected_data = self.test_student_data[expected_id]

                with self.subTest():
                    self.assertEqual(student_repr, expected_data)

    def test_get_students_related_to_group_with_not_existing_id(self):
        for id_ in self.not_existing_id:
            students = self.student_interface.get_students_related_to_group(
                id_
            )

            with self.subTest():
                self.assertEqual(students, [])

    def test_new_student(self):
        new_students_data = [
            {
                'id': 11, 'first_name': 'Oleksii',
                'last_name': 'Kucher', 'group_id': 1
            },

            {
                'id': 12, 'first_name': 'Oleg',
                'last_name': 'Kor', 'group_id': 2
            },

            {
                'id': 13, 'first_name': 'Stas',
                'last_name': 'Nielopov', 'group_id': 3
            }
        ]

        expected_students_repr = [
            'Student id: 11 - Oleksii Kucher, Group id: 1',
            'Student id: 12 - Oleg Kor, Group id: 2',
            'Student id: 13 - Stas Nielopov, Group id: 3'
        ]

        for new_student_data, expected_repr in zip(
                new_students_data, expected_students_repr
        ):
            id_, first_name, last_name, group_id = new_student_data.values()

            self.student_interface.add_new_student(
                id_, group_id, first_name, last_name
            )

            new_student = self.student_interface.get_student_by_id(id_)
            student_repr = str(new_student)

            with self.subTest():
                self.assertEqual(student_repr, expected_repr)

    def test_add_student_to_course(self):
        students_courses_to_add = {
            2: ['Writing', 'German'],
            5: ['Computer studies', 'Writing'],
            7: ['Geography', 'Art']
        }

        expected_courses_repr = {
            2: ["Subject id: 4, name: 'Writing', "
                "description: 'Test description for Writing'",
                "Subject id: 5, name: 'German', "
                "description: 'Test description for German'"],
            5: ["Subject id: 3, name: 'Computer studies', "
                "description: 'Test description for Computer studies'",
                "Subject id: 4, name: 'Writing', "
                "description: 'Test description for Writing'"],
            7: ["Subject id: 1, name: 'Geography', "
                "description: 'Test description for Geography'",
                "Subject id: 2, name: 'Art', "
                "description: 'Test description for Art'"]

        }

        for id_, courses_to_add in students_courses_to_add.items():
            for course in courses_to_add:
                self.student_interface.add_student_to_course(id_, course)

            student = self.student_interface.get_student_with_full_info(id_)

            expected_repr = expected_courses_repr[id_]

            repr_of_student_courses = [
                str(course) for course in student.courses
            ]

            for course_repr in expected_repr:
                with self.subTest():
                    self.assertIn(course_repr, repr_of_student_courses)

    def test_add_student_to_course_with_invalid_data(self):
        for id_ in self.not_existing_id:
            with self.subTest():
                with self.assertRaises(ValueError):
                    self.student_interface.add_student_to_course(
                        id_, 'Art')

        for id_ in self.test_student_data:
            for course in self.not_existing_courses:
                with self.subTest():
                    with self.assertRaises(ValueError):
                        self.student_interface.add_student_to_course(
                            id_, course)

    def test_remove_student_from_course(self):
        students_courses_to_remove = {
            1: ['Computer studies', 'Art'],
            3: ['Geography', 'Writing'],
            8: ['Geography', 'Computer studies']
        }

        expected_courses_repr = {
            1: ["Subject id: 3, name: 'Computer studies', "
                "description: 'Test description for Computer studies'",
                "Subject id: 2, name: 'Art', "
                "description: 'Test description for Art'"],
            3: ["Subject id: 1, name: 'Geography', "
                "description: 'Test description for Geography'",
                "Subject id: 4, name: 'Writing', "
                "description: 'Test description for Writing'"],
            8: ["Subject id: 1, name: 'Geography', "
                "description: 'Test description for Geography'",
                "Subject id: 3, name: 'Computer studies', "
                "description: 'Test description for Computer studies'", ]
        }

        for id_, courses_to_remove in students_courses_to_remove.items():
            for course in courses_to_remove:
                self.student_interface.remove_student_from_course(id_, course)

            student = self.student_interface.get_student_with_full_info(id_)

            expected_repr = expected_courses_repr[id_]

            repr_of_student_courses = [
                str(course) for course in student.courses
            ]

            for course in expected_repr:
                with self.subTest():
                    self.assertNotIn(course, repr_of_student_courses)

    def test_remove_from_course_with_invalid_data(self):
        for id_ in self.not_existing_id:
            with self.subTest():
                with self.assertRaises(ValueError):
                    self.student_interface.remove_student_from_course(
                        id_, 'Art')

        for id_ in self.test_student_data:
            for course in self.not_existing_courses:
                with self.subTest():
                    with self.assertRaises(ValueError):
                        self.student_interface.remove_student_from_course(
                            id_, course)


class TestGroupInterface(InitTestDbForTests):
    group_interface = GroupInterface(engine=test_engine)

    test_groups = {
        1: "Group id: 1, name: 'SD-58'",
        2: "Group id: 2, name: 'TU-69'",
        3: "Group id: 3, name: 'DD-30'",
        4: "Group id: 4, name: 'QK-85'",
        5: "Group id: 5, name: 'CX-73'"
    }

    not_existing_id = [15, 21, 25, 7]

    def test_get_all_groups(self):
        groups = self.group_interface.get_all_groups()

        for group, expected_repr in zip(
            groups, self.test_groups.values()
        ):
            group_repr = str(group.Group)

            with self.subTest():
                self.assertEqual(group_repr, expected_repr)

    def test_get_group_by_id(self):
        for id_, expected_repr in self.test_groups.items():
            group = self.group_interface.get_group_by_id(id_)
            group_repr = str(group)

            with self.subTest():
                self.assertEqual(group_repr, expected_repr)

    def test_get_group_by_id_with_not_existing_id(self):
        for id_ in self.not_existing_id:
            group = self.group_interface.get_group_by_id(id_)

            with self.subTest():
                self.assertIsNone(group)

    def test_check_if_group_exists(self):
        for id_ in self.test_groups:
            result = self.group_interface.check_if_group_exists(id_)

            with self.subTest():
                self.assertTrue(result)

    def test_check_if_group_exists_with_not_existing_id(self):
        for id_ in self.not_existing_id:
            result = self.group_interface.check_if_group_exists(id_)

            with self.subTest():
                self.assertFalse(result)

    def test_group_with_less_students_count(self):
        student_count_groups = {
            1: ["Group id: 5, name: 'CX-73'"],
            2: ["Group id: 2, name: 'TU-69'", "Group id: 3, name: 'DD-30'",
                "Group id: 4, name: 'QK-85'", "Group id: 5, name: 'CX-73'"]
        }

        for count, groups_repr in student_count_groups.items():
            groups = self.group_interface.get_group_with_less_students_count(
                count
            )

            for group, expected_repr in zip(groups, groups_repr):
                group_repr = str(group.Group)

                with self.subTest():
                    self.assertEqual(group_repr, expected_repr)

    def test_group_with_less_students_count_with_incorrect_count(self):
        incorrect_count = [-20, 0, -3]

        for count in incorrect_count:
            groups = self.group_interface.get_group_with_less_students_count(
                count
            )

            with self.subTest():
                self.assertEqual(groups, [])


class TestCourseInterface(InitTestDbForTests):
    courses_interface = CourseInterface()

    test_courses = {
        1: "Subject id: 1, name: 'Arithmetic', "
           "description: 'Test description for Arithmetic'",

        2: "Subject id: 2, name: 'Reading', "
           "description: 'Test description for Reading'",

        3: "Subject id: 3, name: 'Science', "
           "description: 'Test description for Science'",

        4: "Subject id: 4, name: 'Natural history', "
           "description: 'Test description for Natural history'",

        5: "Subject id: 5, name: 'Computer studies', "
           "description: 'Test description for Computer studies'",

        6: "Subject id: 6, name: 'Literacy', "
           "description: 'Test description for Literacy'",

        7: "Subject id: 7, name: 'Music', "
           "description: 'Test description for Music'",

        8: "Subject id: 8, name: 'Art', "
           "description: 'Test description for Art'",

        9: "Subject id: 9, name: 'Social studies', "
           "description: 'Test description for Social studies'",

        10: "Subject id: 10, name: 'History', "
            "description: 'Test description for History'"
    }

    not_existing_id = [11, 15, 21, 221]

    def test_get_all_courses(self):
        courses = self.courses_interface.get_all_courses()

        for course, expected_repr in zip(
            courses, self.test_courses.values()
        ):
            course_repr = str(course.Course)

            with self.subTest():
                self.assertEqual(course_repr, expected_repr)

    def test_get_course_by_id(self):
        for id_, expected_repr in self.test_courses.items():
            course = self.courses_interface.get_course_by_id(id_)
            course_repr = str(course)

            with self.subTest():
                self.assertEqual(course_repr, expected_repr)

    def test_get_course_by_id_with_not_existing_id(self):
        for id_ in self.not_existing_id:
            course = self.courses_interface.get_course_by_id(id_)

            with self.subTest():
                self.assertIsNone(course)


if __name__ == '__main__':
    unittest.main()
