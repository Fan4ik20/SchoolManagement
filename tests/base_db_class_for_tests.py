import unittest
from unittest import mock

from models.manage_school_db import InitSchoolDb, DropSchoolDb

from tests.test_data.test_school_data import test_data
from tests.test_db_settings.settings import test_engine


class InitTestDbForTests(unittest.TestCase):
    @mock.patch(
        'school_generator.'
        'school_data_generator.StudentGenerator.generate_random_students',
        return_value=test_data['students']
    )
    @mock.patch(
        'school_generator.'
        'school_data_generator.GroupGenerator.generate_random_groups_name',
        return_value=test_data['groups']
    )
    @mock.patch(
        'school_generator.'
        'school_data_generator.CoursesGenerator.generate_random_courses',
        return_value=test_data['courses']
    )
    @mock.patch(
        'school_generator.'
        'school_data_generator.AssignStudentCourse.assign_student_to_course',
        return_value=test_data['students_courses']
    )
    @mock.patch(
        'school_generator.'
        'school_data_generator.AssignStudentGroup.assign_student_to_group',
        return_value=test_data['students_group']
    )
    def setUp(self, students, groups, courses,
              students_courses, students_group) -> None:
        InitSchoolDb(engine=test_engine).init_db()

    def tearDown(self) -> None:
        DropSchoolDb(engine=test_engine).drop_tables()
