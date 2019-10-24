"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, session

import hackbright

app = Flask(__name__)
app.secret_key = "SEEKRIT"

@app.route("/student")
def get_student():
    """Show information about a student."""

    if request.args.get('github'):
        github = request.args.get('github')
    else:
        github = session['recent_student_github']

    first, last, github = hackbright.get_student_by_github(github)

    get_grade = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           get_grade=get_grade)

    return html


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/new-student")
def new_student():
    """Display new student addition form"""

    return render_template("add_student.html")


@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)

    session['recent_student_github'] = github

    return render_template("student_added.html", first=first_name, last=last_name)


@app.route("/project")
def list_project_info():
    """List title, description, and max grade of a project."""

    if request.args.get('title'):
        title = request.args.get('title')

    project_info = hackbright.get_project_by_title(title)

    grade_list = hackbright.get_grades_by_title(title)

    html = render_template("project_info.html", project_info=project_info,
                                                grade_list=grade_list)

    return html


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
