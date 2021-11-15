from typing import List

from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload, joinedload

from app import db_engine

from models.models import Course, Group, Student, SchoolBase

from school_generator.school_data_generator import StudentGenerator
from school_generator.school_data_generator import GroupGenerator
from school_generator.school_data_generator import CoursesGenerator
from school_generator.school_data_generator import AssignStudentGroup
from school_generator.school_data_generator import AssignStudentCourse


class SchoolDb:
    """Base class to inherit."""

    def __init__(
            self, course_model=Course, group_model=Group,
            student_model=Student, base=SchoolBase, engine=db_engine
    ):
        self._course_model = course_model
        self._group_model = group_model
        self._student_model = student_model
        self._base = base
        self._engine = engine


class InitSchoolDb(SchoolDb):
    """Class for initialization db and filling with test data."""

    def __init__(self, course_model=Course, group_model=Group,
                 student_model=Student, base=SchoolBase, engine=db_engine):
        super().__init__(course_model, group_model,
                         student_model, base,
                         engine)

        self._groups = GroupGenerator.generate_random_groups_name(10)
        self._courses = CoursesGenerator.generate_random_courses(10)
        self._students = StudentGenerator.generate_random_students(200)

    def _init_group_model(self) -> None:
        groups_list = (
            [self._group_model(name=group_name) for group_name in self._groups]
        )

        with Session(self._engine) as session:
            session.add_all(groups_list)

            session.flush()
            session.commit()

    def _init_course_model(self) -> None:
        courses_list = (
            [self._course_model(name=course,
                                description=f'Test description for {course}')
             for course in self._courses]
        )

        with Session(self._engine) as session:
            session.add_all(courses_list)
            session.flush()
            session.commit()

    def _init_student_courses(self) -> None:
        student_courses = AssignStudentCourse.assign_student_to_course(
            self._students, self._courses
        )

        for student, courses in student_courses.items():
            first_name, last_name = student.split()

            with Session(self._engine) as session:
                # Getting an individual student.
                student_ = session.execute(
                    select(self._student_model).where(
                        self._student_model.first_name == first_name,
                        self._student_model.last_name == last_name
                    )
                ).first()[0]

                for course in courses:
                    # Getting courses for this student.
                    course_ = session.execute(
                        select(self._course_model).where(
                            self._course_model.name == course
                        )
                    ).one()[0]

                    # Assign student to the course.
                    student_.courses.append(course_)

                session.flush()
                session.commit()

    def _init_student_model(self) -> None:
        group_students = AssignStudentGroup.assign_student_to_group(
            self._students, self._groups
        )

        # Student initialization.
        for group, students in group_students.items():
            with Session(self._engine) as session:
                # Obtaining a group ID for subsequent assignment to a student.
                group_id = session.execute(
                    select(
                        self._group_model.id
                    ).where(self._group_model.name == group)
                ).one()[0]

                # Constructing student instances.
                student_list = []
                for student_name in students:
                    first_name, last_name = student_name.split()

                    student_list.append(self._student_model(
                        group_id=group_id, first_name=first_name,
                        last_name=last_name)
                    )

                session.add_all(student_list)
                session.flush()
                session.commit()

        self._init_student_courses()

    def init_db(self) -> None:
        self._base.metadata.create_all(self._engine)

        self._init_group_model()
        self._init_course_model()
        self._init_student_model()

    def test_students(self):
        self._init_student_model()


class DropSchoolDb(SchoolDb):
    def drop_tables(self):
        self._base.metadata.drop_all(self._engine)

    def drop_student_table(self):
        pass

    def drop_group_table(self):
        pass

    def drop_course_table(self):
        pass


class StudentInterface(SchoolDb):
    """Class that provides an interface
    for working with  a Student table in db.

    """

    def get_all_students(self) -> List[Student]:
        with Session(self._engine) as session:
            return session.execute(select(self._student_model)).all()

    def get_student_by_id(self, student_id: int) -> Student:
        with Session(self._engine) as session:
            return session.get(self._student_model, student_id)

    def get_students_related_to_course(
            self, course_name: str) -> List[Student] or None:
        with Session(self._engine) as session:
            course = session.execute(
                select(
                    self._course_model
                ).where(
                    self._course_model.name == course_name
                )
            ).scalar()

            # if course with given name is not exists.
            if not course:
                return None

            students = session.execute(
                select(
                    self._student_model
                ).where(
                    self._student_model.courses.contains(course)
                ).options(
                    selectinload(self._student_model.courses)
                ).order_by(self._student_model.id)
            ).all()

            return students

    def get_student_with_full_info(self, student_id: int) -> Student:
        with Session(self._engine) as session:
            student = session.execute(
                select(
                    self._student_model
                ).where(
                    self._student_model.id == student_id
                ).options(
                    joinedload(self._student_model.group),
                    selectinload(self._student_model.courses)
                )
            ).scalar()

            return student

    def add_new_student(self, id_: int, group_id: int, first_name: str,
                        last_name: str) -> None:
        with Session(self._engine) as session:
            new_student = self._student_model(
                id=id_, group_id=group_id,
                first_name=first_name, last_name=last_name
            )

            session.add(new_student)
            session.flush()
            session.commit()

    def check_if_student_exists(self, student_id: int) -> bool:
        with Session(self._engine) as session:
            return bool(session.get(self._student_model, student_id))

    def add_student_to_course(self, student_id: int, course_name: str) -> None:
        with Session(self._engine) as session:
            if not (student := session.get(self._student_model, student_id)):
                session.rollback()
                raise ValueError(f'Passed invalid student ID ({student_id})!')

            course = session.execute(
                select(
                    self._course_model
                ).where(self._course_model.name == course_name)
            ).scalar()

            if not course:
                session.rollback()
                raise ValueError(
                    f'Passed invalid course name ({course_name})!'
                )

            student.courses.append(course)

            session.flush()
            session.commit()

    def delete_student_by_id(self, student_id: int) -> None:
        with Session(self._engine) as session:
            if not self.check_if_student_exists(student_id):
                session.rollback()
                raise ValueError(f'Passed invalid student ID ({student_id})!')

            session.delete(session.get(self._student_model, student_id))
            session.flush()

            session.commit()

    def remove_student_from_course(
            self, student_id: int, course_name: str) -> None:
        with Session(self._engine) as session:
            if not (student := session.get(self._student_model, student_id)):
                session.rollback()
                raise ValueError(f'Passed invalid student ID ({student_id})!')

            course = session.execute(
                select(
                    self._course_model
                ).where(
                    self._course_model.name == course_name
                )
            ).scalar()

            if not course:
                session.rollback()
                raise ValueError(f'Passed invalid course name! {course_name}')

            student.courses.remove(course)

            session.flush()
            session.commit()

    def get_students_related_to_group(self, group_id: int) -> List[Student]:
        with Session(self._engine) as session:
            group = session.get(self._group_model, group_id)

            students = session.execute(
                select(
                    self._student_model
                ).where(self._student_model.group == group)
            ).all()

            return students


class GroupInterface(SchoolDb):
    """Class that provides an interface
    for working with a Group table in db.

    """

    def get_all_groups(self) -> List[Group]:
        with Session(self._engine) as session:
            return session.execute(select(self._group_model)).all()

    def get_group_by_id(self, group_id: int) -> Group:
        with Session(self._engine) as session:
            return session.get(self._group_model, group_id)

    def get_group_with_less_students_count(
            self, student_count: int) -> List[Group]:
        with Session(self._engine) as session:
            groups = session.execute(
                select(
                    self._group_model, func.count(
                        self._student_model.id
                    ).label('students_count')
                ).join_from(
                    self._group_model, self._student_model
                ).group_by(
                    self._group_model.id
                ).having(
                    func.count('students_count') <= student_count
                ).order_by(self._group_model.id)
            ).all()

            return groups

    def check_if_group_exists(self, group_id: int) -> bool:
        with Session(self._engine) as session:
            return bool(session.get(self._group_model, group_id))


class CourseInterface:
    """Class that provides an interface
        for working with  a Course table in db.

    """

    def __init__(self, course_model=Course, engine=db_engine):
        self._course = course_model
        self._engine = engine

    def get_all_courses(self) -> List[Course]:
        with Session(self._engine) as session:
            return session.execute(select(self._course)).all()

    def get_course_by_id(self, course_id: int) -> Course:
        with Session(self._engine) as session:
            return session.get(self._course, course_id)
