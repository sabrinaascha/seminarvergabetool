from app.models import Student, Wahl, Projekt
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required


bp_student = Blueprint("bp_student", __name__)

@bp_student.route("/")
@login_required
def profil():
    student = Student.get_student(current_user.nds)
    arten = student.get_selected_arten()
    return render_template("student/profil.html",
                           student=student,
                           arten=arten)


@bp_student.route('/themenwahl', methods=['GET', 'POST'])
def themenwahl():
    student = Student.get_student(current_user.nds)
    arten = student.get_selected_arten()
    selected_art = request.args.get('art_typ', arten[0].art_typ if arten else None)

    if request.method == 'POST':
        priorities = [
            (request.form.get('prio1'), 1),
            (request.form.get('prio2'), 2),
            (request.form.get('prio3'), 3),
        ]

        priorities = [(int(p[0]), p[1]) for p in priorities if p[0]]
        Wahl.save_priorities(student.stud_id, priorities)

        return redirect(url_for('bp_themen.themenwahl', art_typ=selected_art))

    projekte = Projekt.get_projects_by(art_filter=selected_art) if selected_art else []
    return render_template('student/themenwahl.html',
                           projekte=projekte,
                           arten=arten,
                           selected_art=selected_art)