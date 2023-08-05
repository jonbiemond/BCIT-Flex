"""Console interface and GUI to get data from the db."""
import re

import PySimpleGUI as sg
from sqlalchemy.orm import Session

from bcitflex.model import Course, Subject
from bcitflex.model.db_config import session


def valid_subject(session: Session, subject_id: str) -> bool:
    """Check subject exists in database."""
    return session.get(Subject, subject_id) is not None


def get_valid_course(subject: Subject) -> Course:
    course_code = input("Enter a course code: ").strip().lower()

    while not subject.has_course(course_code):
        if not re.match(r"^\d{4}$", course_code):
            msg = "Course codes must be 4 digits long"
        else:
            msg = f'"{course_code}" is not a valid course for "{subject.name()}"'
        course_code = input(msg + ", please try again: ").strip().lower()

    return subject.get_course(course_code)


def set_theme(name: str = "Violet"):
    violet = {
        "BACKGROUND": "#1A1F30",
        "TEXT": "#B9C3CD",
        "INPUT": "#281E32",
        "TEXT_INPUT": "#B9C3CD",
        "SCROLL": "#173D59",
        "BUTTON": ("#E18CF5", "#202040"),
        "PROGRESS": ("#000000", "#000000"),
        "BORDER": 1,
        "SLIDER_DEPTH": 0,
        "PROGRESS_DEPTH": 0,
        "COLOR_LIST": ["#202040", "#1A1F30", "#281E32", "#B9C3CD"],
    }

    sg.theme_add_new("Violet", violet)
    sg.theme(name)


def simple_gui():
    courses = []

    set_theme()

    dropdown = sg.Combo(
        courses,
        size=(24, 1),
        expand_x=True,
        enable_events=True,
        readonly=True,
        key="-COMBO-",
    )
    layout = [
        [
            sg.Push(),
            sg.Text("Subject"),
            sg.InputText(size=(20, 1), key="-IN-"),
            sg.Submit("Load"),
        ],
        [sg.Push(), sg.Text("Course"), dropdown],
        [sg.Text(size=(19, 1), key="-OUT-")],
        [sg.Cancel()],
    ]

    window = sg.Window("BCIT Course Finder", layout, icon=r"images\search_page.ico")

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Cancel"):
            break

        if event == "Load":
            subject_id = values["-IN-"].upper()
            if subject_id:
                if not valid_subject(session, subject_id):
                    sg.popup(f'"{subject_id}" is not a valid subject.', title="Error")
                    continue

                window["-OUT-"].update(f"Loading {subject_id} courses...")
                window.refresh()

                subject = session.get(Subject, subject_id)

                window["-OUT-"].update(f"{subject_id} courses loaded.")
                courses = [
                    f"{subject_id} {course.code} ({course.offering_count(True)}/{course.offering_count()})"
                    for course in subject.courses
                ]
                courses.sort()
                window["-COMBO-"].update(values=courses)
                window.refresh()

            else:
                sg.popup("Please enter a subject.", title="Error")

        if event == "-COMBO-":
            course_code = values["-COMBO-"].split(" ")[1]
            if course_code:
                subject_id = values["-IN-"].upper()
                subject = session.get(Subject, subject_id)
                course = subject.get_course(course_code)
                sg.popup_scrolled(
                    course.to_string(),
                    title=f"{subject_id.upper()} {course.code}",
                    font="Courier 10",
                    size=(80, 30),
                )

    window.close()


def console_input():
    raise NotImplementedError
    subject_name = valid_subject()
    subject = Subject(subject_name)
    course = get_valid_course(subject)
    print(course)


if __name__ == "__main__":
    simple_gui()
