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
    layout = [
        [sg.Text("Enter a subject: ", key='-INSTRUCTION-')],
        [sg.InputText(key="-IN-")],
        [sg.Text(size=(19, 1), key="-OUT-")],
        [sg.Submit(), sg.Cancel(), sg.Button("Back", visible=False)]
    ]

    window = sg.Window("BCIT Course Finder", layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Cancel"):
            break
        if event == "Submit":
            subject_code = values["-IN-"]
            if subject_code:
                window["-OUT-"].update(f'Loading {subject_code} courses...')
                window.refresh()

                subject = Subject(subject_code)

                window["-OUT-"].update('')
                window["-IN-"].update('')
                window.refresh()

                window["-INSTRUCTION-"].update("Enter a course code: ")
                window["Back"].update(visible=True)

                while True:
                    event, values = window.read()
                    if event in (sg.WIN_CLOSED, "Cancel"):
                        break
                    elif event == "Back":
                        window["-IN-"].update('')
                        window["-INSTRUCTION-"].update("Enter a subject: ")
                        window["Back"].update(visible=False)
                        break
                    if event == "Submit":
                        course_code = values["-IN-"]
                        if course_code:
                            if subject.has_course(course_code):
                                course = subject.get_course(course_code)
                                sg.popup_scrolled(course.to_string(), title=course.code())
                            else:
                                sg.popup_scrolled(f"\"{course_code}\" is not a valid course for \"{subject_code}\"")
                        else:
                            sg.popup_scrolled("Please enter a course code.")
            else:
                sg.popup_scrolled("Please enter a subject.")

    window.close()


def console_input():
    subject_name = valid_subject()
    subject = Subject(subject_name)
    course = get_valid_course(subject)
    print(course.to_string())


if __name__ == '__main__':
    simple_gui()
