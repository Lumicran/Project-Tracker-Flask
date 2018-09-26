"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route('/')
def show_homepage():
    students = hackbright.get_all_students()
    projects = hackbright.get_all_projects()

    return render_template("homepage.html",
                            students = students,
                            projects = projects)


@app.route('/student_search')
def show_student_search():
    return render_template("student_search.html")

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    projects = hackbright.get_grades_by_github(github)
    
    return render_template("student_info.html",
                            first = first,
                            last = last,
                            github = github,
                            projects = projects)

@app.route("/student_form")
def show_student_form():
    """Show form to make a new student."""

    return render_template("make_new_student.html")

@app.route("/student_add", methods=['POST'])
def student_add():
    """Add a student."""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    github = request.form.get("github")

    hackbright.make_new_student(first_name, last_name, github)

    return render_template("add_student_success.html",
                            first_name = first_name,
                            last_name = last_name,
                            github = github)

@app.route("/project")
def show_project_listing():
    """Show projects"""

    title = request.args.get('title')

    row = hackbright.get_project_by_title(title)

    grades = hackbright.get_grades_by_title(title)

    return render_template("project_listing.html",
                            project = row,
                            grades = grades)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
