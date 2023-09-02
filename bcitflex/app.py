"""Web app"""
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bcitflex.app_functions import filter_courses
from bcitflex.model import Base, Course

app = Flask(__name__)

engine = create_engine("postgresql://python_app@localhost:5432/bcitflex")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route("/")
@app.route("/courses")
def show_courses():
    courses = session.query(Course).all()
    return render_template("courses.html", courses=courses)


@app.route("/courses/<int:course_id>")
def show_course(course_id):
    course = session.get(Course, course_id)
    return render_template("course.html", course=course)


@app.route("/courses/query", methods=["GET", "POST"])
def query_courses():
    if request.method == "POST":
        subject = request.form.get("subject")
        course_code = request.form.get("course_code")
        available = request.form.get("available")

        courses = filter_courses(
            session=session,
            subject=subject,
            course_code=course_code,
            available=available,
        )

        return render_template("courses.html", courses=courses)
    else:
        return render_template("query_courses.html")


if __name__ == "__main__":
    app.run()
