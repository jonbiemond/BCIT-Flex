import re
import PySimpleGUI as sg

from modules.course import Course
from modules.subject import Subject


def valid_subject() -> str:
    subject = input("Enter a subject: ").strip().lower()

    while subject not in open("subjects.txt").read().splitlines():
        subject = input(f"\"{subject}\" is not a valid subject, please try again ").strip().lower()

    return subject


def get_valid_course(subject: Subject) -> Course:
    course_code = input("Enter a course code: ").strip().lower()

    while not subject.has_course(course_code):
        if not re.match(r"^\d{4}$", course_code):
            msg = "Course codes must be 4 digits long"
        else:
            msg = f"\"{course_code}\" is not a valid course for \"{subject.name()}\""
        course_code = input(msg + ", please try again: ").strip().lower()

    return subject.get_course(course_code)


def simple_gui():
    subjects = {}
    courses = []
    dropdown = sg.Combo(courses, expand_x=True, enable_events=True, readonly=False, key='-COMBO-')
    layout = [
        [sg.Text("Enter a subject: ", key='-INSTRUCTION-')],
        [sg.InputText(key="-IN-")],
        [dropdown],
        [sg.Text(size=(19, 1), key="-OUT-")],
        [sg.Submit("Load"), sg.Button("Save"), sg.Cancel()]
    ]

    window = sg.Window("BCIT Course Finder", layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Cancel"):
            break

        if event in ["Load", "Save"]:
            subject_code = values["-IN-"]
            if subject_code:
                window["-OUT-"].update(f'Loading {subject_code.upper()} courses...')
                window.refresh()

                if subject_code in subjects:
                    subject = subjects[subject_code]
                else:
                    subject = Subject(subject_code)
                    subjects[subject_code] = subject

                window["-OUT-"].update(f'{subject_code.upper()} courses loaded.')
                courses = [f'{course.code()} ({course.offering_count()})' for course in subject.courses()]
                courses.sort()
                window["-COMBO-"].update(values=courses)
                window.refresh()

                if event == "Save":
                    filename = subject.to_file()
                    sg.popup_scrolled(f"Saved courses to \"{filename}\"", title="Success")

            else:
                sg.popup_scrolled("Please enter a subject.")

        if event == "-COMBO-":
            course_code = values["-COMBO-"].split(" ")[0]
            if course_code:
                subject_code = values["-IN-"]
                subject = subjects[subject_code]
                course = subject.get_course(course_code)
                sg.popup_scrolled(course.to_string(), title=course.code())

    window.close()


def console_input():
    subject_name = valid_subject()
    subject = Subject(subject_name)
    course = get_valid_course(subject)
    print(course.to_string())


if __name__ == '__main__':
    simple_gui()
