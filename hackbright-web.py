from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route('/')
def get_all():
    """lists students and projects."""

    # return render_template("student_search.html")
    students = hackbright.get_all_students()
    projects = hackbright.get_all_projects()
    return render_template("home.html",
                    students=students,
                    projects=projects)

@app.route('/student-search')
def get_student_form():
    """Show form for searching for a student."""
    return render_template("student_search.html")


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    grades = hackbright.get_grades_by_github(github)
    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           grades=grades)
    return html

@app.route('/add')
def get_new_student():
    """Show form for adding a student."""

    return render_template("student_creation.html")


@app.route('/project-search')
def get_project():
    """Show form for adding a student."""

    return render_template("project_search.html")


@app.route('/project')
def show_project():
    """Show Project info."""
    title = request.args.get('project')
    title, description, max_grade = hackbright.get_project_by_title(title)
    students = hackbright.get_grades_by_title(title)
    return render_template("project_info.html",
                            title=title,
                            description=description,
                            max_grade=max_grade,
                            students=students)


@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student to database."""

    github = request.form.get('github')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    hackbright.make_new_student(fname, lname, github)
    html = render_template("add_confirmation.html",
                           first=fname,
                           last=lname,
                           github=github)
    return html

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
