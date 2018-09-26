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

@app.route('/assign_grade_form')
def show_assign_grade_form():
    """Form to assign a grade to a student."""

    students = hackbright.get_all_students()
    projects = hackbright.get_all_projects()

    return render_template('assign_grade_form.html',
                            students = students,
                            projects = projects)

@app.route('/grade_update', methods=['POST'])
def update_grade():

    github = request.form.get("student")
    title = request.form.get("project")
    project = hackbright.get_project_by_title(title)
    max_grade = project[2]

    grade = hackbright.get_grade_by_github_title(github, title)
    
    if grade == None:
        print("grade is empty")
    else:
        print("grade exists")

    return github



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


@app.route("/project_form")
def show_project_form():
    """Show form to make a new project."""

    return render_template("make_new_project.html")

@app.route("/project_add", methods=['POST'])
def project_add():
    """Add a project."""

    title = request.form.get("title")
    description = request.form.get("description")
    max_grade = request.form.get("max_grade")

    hackbright.make_new_project(title, description, max_grade)

    return render_template("add_project_success.html",
                            title = title,
                            description = description,
                            max_grade = max_grade)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
