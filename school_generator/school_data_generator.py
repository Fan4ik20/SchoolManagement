from random import choices, randint, choice, sample
import string


class GroupGenerator:
    _letters = string.ascii_uppercase

    @classmethod
    def generate_random_groups_name(cls, count: int) -> list:
        return (
            [f'{"".join(choices(cls._letters, k=2))}'
             f'-{randint(0, 9)}{randint(0, 9)}' for _ in range(count)]
        )


class StudentGenerator:
    _first_names = [
        'Liam', 'Olivia',
        'Noah', 'Emma',
        'Oliver', 'Ava',
        'Elijah', 'Charlotte',
        'William', 'Sophia',
        'James', 'Amelia',
        'Benjamin', 'Isabella',
        'Lucas', 'Mia',
        'Henry', 'Evelyn',
        'Alexander', 'Harper',
    ]

    _last_names = [
        'Smith', 'Johnson',
        'Williams', 'Brown',
        'Jones', 'Miller',
        'Davis', 'Garcia',
        'Rodriguez', 'Wilson',
        'Martinez', 'Anderson',
        'Taylor', 'Thomas',
        'Hernande', 'Moore',
        'Martin', 'Jackson',
        'Thompson', 'White',
    ]

    @classmethod
    def generate_random_students(cls, count: int) -> list:
        return [f'{choice(cls._first_names)} {choice(cls._last_names)}'
                for _ in range(count)]


class CoursesGenerator:
    _courses = [
        'Art', 'Citizenship',
        'Geography', 'History',
        'French', 'German',
        'Literacy', 'Music',
        'Natural history', 'Science',
        'Arithmetic', 'Social studies',
        'Reading', 'Writing',
        'Math', 'Business studies',
        'Drama', 'Modern studies',
        'Computer studies', 'Chemistry',
        ]

    @classmethod
    def generate_random_courses(cls, count: int):
        if count > len(cls._courses):
            raise ValueError(f'Max count is - {len(cls._courses)}')

        return sample(cls._courses, count)


class AssignStudentGroup:
    @staticmethod
    def assign_student_to_group(students: list, groups: list):
        group_students = {}

        not_assigned_students = students[:]

        for group in groups:
            group_students[group] = []

            for _ in range(randint(10, 30)):
                if len(not_assigned_students) <= 0:
                    return group_students

                random_student = (
                    not_assigned_students.pop(
                        randint(0, len(not_assigned_students) - 1))
                )

                group_students[group].append(random_student)
        return group_students


class AssignStudentCourse:
    @staticmethod
    def assign_student_to_course(students: list, courses: list):
        student_courses = {}

        for student in students:
            courses_for_student = sample(courses, randint(1, 3))

            student_courses[student] = courses_for_student

        return student_courses


def main():
    groups = GroupGenerator.generate_random_groups_name(10)
    students = StudentGenerator.generate_random_students(10)
    group_students = AssignStudentGroup.assign_student_to_group(
        students, groups
    )

    courses = CoursesGenerator.generate_random_courses(10)


if __name__ == '__main__':
    main()
