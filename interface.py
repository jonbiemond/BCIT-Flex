from modules.course import Course
from modules.subject import Subject


def valid_subject() -> str:
    subject = input("Enter a subject: ").strip().lower()

    while subject not in open("subjects.txt").read().splitlines():
        subject = input(f"\"{subject}\" is not a valid subject, please try again ").strip().lower()

    return subject


def get_valid_course(subject: Subject) -> Course:
    course = input("Enter a course: ").strip().lower()

    while not subject.has_course(course):
        course = input(f"\"{course}\" is not a valid course, please try again: ").strip().lower()

    return subject.get_course(course)


def main():
    subject_name = valid_subject()
    subject = Subject(subject_name)
    course = get_valid_course(subject)
    print(course.name())


if __name__ == '__main__':
    main()
