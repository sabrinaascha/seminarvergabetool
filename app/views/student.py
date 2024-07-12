from app.models import Student, Wahl, Projekt, Phase, Studiengang
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from app.helper import within_prioritization_period, within_registration_period

# definition of the authentication blueprint
bp_student = Blueprint("bp_student", __name__)


@bp_student.route("/", methods=['GET'])
@login_required
def profil():
    # returns the students information based on the nds
    student = Student.get_student(current_user.nds)

    arten = []
    all_priorities = {}

    # check if the student is already registered, if yes selected arten and his eventually available prioritization
    if student:
        arten = student.get_selected_arten()
        all_priorities = Wahl.get_all_priorities(student_id=student.stud_id)

    # get the current phase and true/false if phase 1 or 2 is already active for jinja-querys e.g to display buttons
    current = Phase.get_current()
    phase1_active = current.p1_active()
    phase2_active = current.p2_active()

    return render_template("student/profil.html",
                           student=student,
                           arten=arten,
                           all_priorities=all_priorities,
                           phase1_active=phase1_active,
                           phase2_active=phase2_active)


@bp_student.route('/register', methods=['GET', 'POST'])
@within_registration_period
@login_required
def register():
    # retrieve all study programs
    studiengaenge = Studiengang.get_all_studiengaenge()

    # check if the student is already registered
    student = Student.get_student(current_user.nds)

    if student:
        # if registered, get selected types of work and render already registered template
        arten = student.get_selected_arten()
        return render_template('student/already_registered.html',
                               student=student,
                               arten=arten)

    if request.method == 'POST':
        # other information (mail, nds, name,..) get prefilled from current user
        matrikelnummer = request.form.get('matrikelnummer')
        studiengang_id = request.form.get('studiengang')


        student = Student.create_student(
            vorname=current_user.vorname,
            nachname=current_user.nachname,
            nds=current_user.nds,
            email=current_user.mail,
            matrikelnummer=matrikelnummer,
            studiengang_id=studiengang_id
        )

        # add selected types of work to the just created student
        arten_ids = request.form.getlist('arten')
        student.add_arten(arten_ids)

        arten = student.get_selected_arten()
        return render_template('student/already_registered.html',
                               student=student,
                               arten=arten)

    return render_template('student/register.html',
                           current_user=current_user,
                           studiengaenge=studiengaenge)


@login_required
@within_prioritization_period
@bp_student.route('/themenwahl', methods=['GET', 'POST'])
def themenwahl():
    # getting the student information based on the users nds and their selected types of work
    user = Student.get_student(current_user.nds)
    arten = user.get_selected_arten()

    # if student did not register or didnt select any type of work within his registration, topic selection is not
    # allowed
    if not arten or user is None:
        return redirect(url_for('bp_student.not_possible'))

    # get the selected type of work (as the student can switch with a button through his selected arten)
    selected_art_id = int(request.args.get('art_id', arten[0].art_id))
    selected_art = next((art for art in arten if art.art_id == selected_art_id), None)

    # retrieve the priorities for the selected type of work
    priorities = Wahl.get_priorities_for_art(student_id=user.stud_id,
                                             art_id=selected_art.art_id) if selected_art else None

    if request.method == 'POST':
        priorities = {
            1: request.form.get('prio1'),
            2: request.form.get('prio2'),
            3: request.form.get('prio3')
        }
        Wahl.save_priorities(student_id=user.stud_id, art_id=selected_art.art_id, priorities=priorities)
        return redirect(url_for('bp_student.themenwahl', art_id=selected_art.art_id))

    projekte = Projekt.get_projects_by(art_filter=selected_art.art_typ) if selected_art else []

    return render_template('student/themenwahl.html',
                           projekte=projekte,
                           arten=arten,
                           selected_art=selected_art,
                           priorities=priorities)


# render the error page for when topic selection is not possible (no registration)
@login_required
@bp_student.route('/not_possible', methods=['GET'])
def not_possible():
    return render_template('error/themenwahl_not_possible.html')
