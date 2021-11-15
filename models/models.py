from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

SchoolBase = declarative_base()


course_student = Table(
    'course_student', SchoolBase.metadata,
    Column('course_id', Integer, ForeignKey('course.id')),
    Column('student_id', Integer, ForeignKey('student.id'))
)


class Group(SchoolBase):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)

    students = relationship('Student', back_populates='group')

    def __repr__(self):
        return f'Group id: {self.id}, name: {self.name!r}'


class Student(SchoolBase):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    group_id = Column(ForeignKey('group.id'))

    first_name = Column(String(30), nullable=False)
    last_name = Column(String(40), nullable=False)

    courses = relationship(
        'Course', secondary=course_student, backref='students',
        order_by='Course.id'
    )

    group = relationship('Group', back_populates='students')

    def __repr__(self):
        return (
            f'Student id: {self.id} - {self.first_name} {self.last_name}, '
            f'Group id: {self.group_id}'
        )


class Course(SchoolBase):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), unique=True)
    description = Column(String)

    def __repr__(self):
        return (f'Subject id: {self.id}, name: {self.name!r}, '
                f'description: {self.description!r}')
