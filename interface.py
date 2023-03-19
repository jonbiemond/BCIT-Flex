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
        [sg.Submit(), sg.Button("To File"), sg.Button("Back", visible=False), sg.Cancel()]
    ]

    subjects = {}

    window = sg.Window("BCIT Course Finder", layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Cancel"):
            break

        if event in ["Submit", "To File"]:
            subject_code = values["-IN-"]
            if subject_code:
                window["-OUT-"].update(f'Loading {subject_code.upper()} courses...')
                window.refresh()

                if subject_code in subjects:
                    subject = subjects[subject_code]
                else:
                    subject = Subject(subject_code)
                    subjects[subject_code] = subject

                window["-OUT-"].update('')
                window.refresh()

                if event == "Submit":
                    window["-IN-"].update('')
                    window.refresh()

                    window["-INSTRUCTION-"].update(f"Enter a {subject_code.upper()} course code: ")
                    window["Back"].update(visible=True)
                    window["To File"].update(visible=False)

                    while True:
                        event, values = window.read()
                        if event in (sg.WIN_CLOSED, "Cancel"):
                            break

                        elif event == "Back":
                            window["-IN-"].update('')
                            window["-INSTRUCTION-"].update("Enter a subject: ")
                            window["Back"].update(visible=False)
                            window["To File"].update(visible=True)
                            break

                        elif event == "To File":
                            filename = subject.to_file()
                            sg.popup_scrolled(f"Saved courses to \"{filename}\"", title="Success")

                        elif event == "Submit":
                            course_code = values["-IN-"]
                            if course_code:
                                if subject.has_course(course_code):
                                    course = subject.get_course(course_code)
                                    sg.popup_scrolled(course.to_string(), title=course.code())
                                else:
                                    sg.popup_scrolled(f"\"{course_code}\" is not a valid course for \"{subject_code}\"")
                            else:
                                sg.popup_scrolled("Please enter a course code.")

                elif event == "To File":
                    filename = subject.to_file()
                    sg.popup_scrolled(f"Saved courses to \"{filename}\"", title="Success")

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
