from flask import Blueprint, render_template, request, url_for, redirect, session
from flask_login import current_user, login_required
from app.helper import mitarbeiter_required, superuser_required
from app.models import Projekt, Art, Lehrstuhl, Mitarbeiter, Fach, Studiengang, Phase, Student, Wahl

# definition of the mitarbeiter blueprint
bp_mitarbeiter = Blueprint("bp_mitarbeiter", __name__)


# route for the employee profile
@bp_mitarbeiter.route("/", methods=['GET'])
@login_required
@mitarbeiter_required
def profil():
    # get current employee and their chairs projects
    mitarbeiter = Mitarbeiter.get_mitarbeiter(current_user.nds)
    projekte = mitarbeiter.lehrstuhl.get_lehrstuhl_projekte()
    projekte = Projekt.order_ascending_by_name(projekte)
    session['is_admin'] = False  # set admin status initially to false (gets true when rendering to admin panel)
    return render_template("mitarbeiter/profil.html", mitarbeiter=mitarbeiter, projekte=projekte)


# route for the admin panel
@bp_mitarbeiter.route("/admin", methods=['GET'])
@login_required
@superuser_required
def admin():
    # get all employees, types of work, chairs, projects, students, and current phases
    mitarbeiter = Mitarbeiter.get_all_Mitarbeiter()
    mitarbeiter_dict = Mitarbeiter.group_by_lehrstuhl(mitarbeiter)
    arten = Art.get_all_arten()
    lehrstuehle = Lehrstuhl.get_all_lehrstuehle()
    projekte = Projekt.order_ascending_by_name(Projekt.query.all())
    projekte_dict = Projekt.group_by_lehrstuhl(projekte)
    students = Student.get_all_Students()
    phasen = Phase.get_current()
    session['is_admin'] = True  # set admin status to true
    return render_template('mitarbeiter/admin.html', mitarbeiter_dict=mitarbeiter_dict, lehrstuehle=lehrstuehle,
                           arten=arten, students=students, projekte_dict=projekte_dict, phasen=phasen)


# route for adding a project
@bp_mitarbeiter.route('/add_projekt', methods=['GET', 'POST'])
@login_required
@mitarbeiter_required
def add_projekt():
    # get all types of work, study programs, subjects, chairs, and employees
    arten = Art.get_all_arten()
    studiengaenge = Studiengang.get_all_studiengaenge()
    faecher = Fach.get_all_faecher()
    lehrstuehle = Lehrstuhl.get_all_lehrstuehle()
    mitarbeiter = Mitarbeiter.get_all_Mitarbeiter()
    user = Mitarbeiter.get_mitarbeiter(current_user.nds)
    is_admin = session.get('is_admin', False)

    if request.method == 'POST':
        titel = request.form.get('titel')
        beschreibung = request.form.get('beschreibung')
        studiengang_id = request.form.get('studiengang')
        art_id = int(request.form.get('art'))
        # bachelorthesis and masterthesis always is only for 1 person
        max_anzahl = 1 if art_id in [1, 3] else int(request.form.get('max_anzahl', 1))
        fach_id = request.form.get('fach')
        betreuer_ids = request.form.getlist('betreuer')
        # lehrstuhl_id is preselected with the users chair if is_admin is false
        lehrstuhl_id = request.form.get('lehrstuhl') if is_admin else user.lehrstuhl_lehrstuhl_id

        Projekt.create_projekt(
            titel=titel,
            beschreibung=beschreibung,
            max_anzahl=max_anzahl,
            studiengang_id=studiengang_id,
            fach_id=fach_id,
            lehrstuhl_id=lehrstuhl_id,
            art_id=art_id,
            betreuer_ids=betreuer_ids
        )
        return redirect(url_for('bp_mitarbeiter.admin' if is_admin else 'bp_mitarbeiter.profil'))

    return render_template('forms/projekt_form.html',
                           mitarbeiter=mitarbeiter,
                           studiengaenge=studiengaenge,
                           arten=arten, faecher=faecher,
                           lehrstuehle=lehrstuehle,
                           user=user,
                           is_admin=is_admin)


# route for editing a project
@bp_mitarbeiter.route('/edit/<int:projekt_id>', methods=['GET', 'POST'])
@login_required
@mitarbeiter_required
def edit_projekt(projekt_id):
    user = Mitarbeiter.get_mitarbeiter(current_user.nds)
    projekt = Projekt.query.get(projekt_id)
    studiengaenge = Studiengang.get_all_studiengaenge()
    arten = Art.get_all_arten()
    faecher = Fach.get_all_faecher()
    lehrstuehle = Lehrstuhl.get_all_lehrstuehle()
    mitarbeiter = Mitarbeiter.get_all_Mitarbeiter()
    is_admin = session.get('is_admin', False)

    if request.method == 'POST':
        titel = request.form.get('titel')
        beschreibung = request.form.get('beschreibung')
        studiengang_id = request.form.get('studiengang')
        fach_id = request.form.get('fach')
        art_id = int(request.form.get('art'))
        max_anzahl = 1 if art_id in [1, 3] else int(request.form.get('max_anzahl', 1))
        betreuer_ids = request.form.getlist('betreuer')
        lehrstuhl_id = request.form.get('lehrstuhl') if is_admin else user.lehrstuhl_lehrstuhl_id

        projekt.edit_projekt(titel=titel, beschreibung=beschreibung, max_anzahl=max_anzahl,
                             studiengang_id=studiengang_id, fach_id=fach_id, lehrstuhl_id=lehrstuhl_id, art_id=art_id,
                             betreuer_ids=betreuer_ids)
        return redirect(url_for('bp_mitarbeiter.admin' if is_admin else 'bp_mitarbeiter.profil'))

    return render_template('forms/projekt_form.html',
                           projekt=projekt,
                           mitarbeiter=mitarbeiter,
                           studiengaenge=studiengaenge,
                           lehrstuehle=lehrstuehle,
                           arten=arten,
                           faecher=faecher,
                           user=user,
                           is_admin=is_admin)


# route for deleting a project
@bp_mitarbeiter.route('/delete/<int:projekt_id>', methods=['GET', 'POST'])
@login_required
@mitarbeiter_required
def delete_projekt(projekt_id):
    projekt = Projekt.query.get_or_404(projekt_id)
    is_admin = session.get('is_admin', False)

    if request.method == 'POST':
        if 'confirm' in request.form:
            # delete the project
            projekt.delete_projekt()
        return redirect(url_for('bp_mitarbeiter.admin' if is_admin else 'bp_mitarbeiter.profil'))

    return render_template('forms/confirm_delete.html', projekt=projekt)


# route for adding an employee
@bp_mitarbeiter.route('/add_mitarbeiter', methods=['GET', 'POST'])
@login_required
@mitarbeiter_required
def add_mitarbeiter():
    user = Mitarbeiter.get_mitarbeiter(current_user.nds)
    lehrstuehle = Lehrstuhl.get_all_lehrstuehle()
    is_admin = session.get('is_admin', False)

    if request.method == 'POST':
        # handle form submission for adding an employee
        vorname = request.form.get('vorname')
        nachname = request.form.get('nachname')
        nds = request.form.get('nds')
        email = request.form.get('email')
        lehrstuhl_id = request.form.get('lehrstuhl') if is_admin else user.lehrstuhl_lehrstuhl_id

        # create a new employee
        mitarbeiter = Mitarbeiter.create_mitarbeiter(vorname=vorname, nachname=nachname, nds=nds, email=email,
                                                     lehrstuhl_id=lehrstuhl_id)
        return redirect(url_for('bp_mitarbeiter.admin' if is_admin else 'bp_mitarbeiter.profil'))

    return render_template('forms/mitarbeiter_form.html', lehrstuehle=lehrstuehle, is_admin=is_admin)


# route for editing an employee
@bp_mitarbeiter.route('/edit_mitarbeiter/<int:ma_id>', methods=['GET', 'POST'])
@login_required
@mitarbeiter_required
def edit_mitarbeiter(ma_id):
    user = Mitarbeiter.get_mitarbeiter(current_user.nds)
    mitarbeiter = Mitarbeiter.query.get_or_404(ma_id)
    lehrstuehle = Lehrstuhl.get_all_lehrstuehle()
    is_admin = session.get('is_admin', False)

    if request.method == 'POST':
        vorname = request.form.get('vorname')
        nachname = request.form.get('nachname')
        email = request.form.get('email')
        nds = request.form.get('nds')
        lehrstuhl_id = request.form.get('lehrstuhl') if is_admin else user.lehrstuhl_lehrstuhl_id

        mitarbeiter.edit_mitarbeiter(vorname=vorname, nachname=nachname, email=email, nds=nds,
                                     lehrstuhl_id=lehrstuhl_id)
        return redirect(url_for('bp_mitarbeiter.admin' if is_admin else 'bp_mitarbeiter.profil'))

    return render_template('forms/mitarbeiter_form.html', mitarbeiter=mitarbeiter, lehrstuehle=lehrstuehle,
                           is_admin=is_admin)


# route for deleting an employee
@bp_mitarbeiter.route('/delete_mitarbeiter/<int:ma_id>', methods=['GET', 'POST'])
@login_required
@mitarbeiter_required
def delete_mitarbeiter(ma_id):
    mitarbeiter = Mitarbeiter.query.get_or_404(ma_id)
    is_admin = session.get('is_admin', False)

    if request.method == 'POST':
        if 'confirm' in request.form:
            mitarbeiter.delete_mitarbeiter()
        if is_admin:
            return redirect(url_for('bp_mitarbeiter.admin'))
        else:
            return redirect(url_for('bp_mitarbeiter.profil'))

    return render_template('forms/confirm_delete.html', mitarbeiter=mitarbeiter)


# route for adding a chair
@bp_mitarbeiter.route('/add_lehrstuhl', methods=['GET', 'POST'])
@login_required
@superuser_required
def add_lehrstuhl():
    is_admin = session.get('is_admin', False)

    if request.method == 'POST':
        name = request.form.get('name')
        homepage = request.form.get('homepage')
        professor = request.form.get('professor')

        Lehrstuhl.create_lehrstuhl(name=name, homepage=homepage, professor=professor)
        return redirect(url_for('bp_mitarbeiter.admin'))

    return render_template('forms/lehrstuhl_form.html')


# route for editing a chair
@bp_mitarbeiter.route('/edit_lehrstuhl/<int:lehrstuhl_id>', methods=['GET', 'POST'])
@login_required
@superuser_required
def edit_lehrstuhl(lehrstuhl_id):
    lehrstuhl = Lehrstuhl.query.get_or_404(lehrstuhl_id)

    if request.method == 'POST':
        name = request.form.get('name')
        homepage = request.form.get('homepage')
        professor = request.form.get('professor')

        lehrstuhl.edit_lehrstuhl(name=name, homepage=homepage, professor=professor)
        return redirect(url_for('bp_mitarbeiter.admin'))

    return render_template('forms/lehrstuhl_form.html', lehrstuhl=lehrstuhl)


# route for deleting a chair
@bp_mitarbeiter.route('/delete_lehrstuhl/<int:lehrstuhl_id>', methods=['GET', 'POST'])
@login_required
@superuser_required
def delete_lehrstuhl(lehrstuhl_id):
    lehrstuhl = Lehrstuhl.query.get_or_404(lehrstuhl_id)
    if request.method == 'POST':
        if 'confirm' in request.form:
            lehrstuhl.delete_lehrstuhl()
        return redirect(url_for('bp_mitarbeiter.admin'))

    return render_template('forms/confirm_delete.html', lehrstuhl=lehrstuhl)


# route for adding a student
@bp_mitarbeiter.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    studiengaenge = Studiengang.get_all_studiengaenge()

    if request.method == 'POST':
        vorname = request.form.get('vorname')
        nachname = request.form.get('nachname')
        nds = request.form.get('nds')
        email = request.form.get('email')
        matrikelnummer = request.form.get('matrikelnummer')
        studiengang_id = request.form.get('studiengang')
        art_ids = request.form.getlist('arten')
        student = Student.create_student(vorname=vorname, nachname=nachname, nds=nds, email=email,
                                         matrikelnummer=matrikelnummer, studiengang_id=studiengang_id)
        student.add_arten(arten_ids=art_ids)
        return redirect(url_for('bp_mitarbeiter.admin'))

    return render_template('forms/student_form.html', studiengaenge=studiengaenge)


# route for editing a student
@bp_mitarbeiter.route('/edit_student/<int:stud_id>', methods=['GET', 'POST'])
@login_required
@superuser_required
def edit_student(stud_id):
    student = Student.query.get_or_404(stud_id)
    studiengaenge = Studiengang.get_all_studiengaenge()
    arten = Art.get_all_arten()
    selected_arten = student.get_selected_arten()
    all_priorities = Wahl.get_all_priorities(student_id=student.stud_id)

    if request.method == 'POST':
        vorname = request.form.get('vorname')
        nachname = request.form.get('nachname')
        nds = request.form.get('nds')
        email = request.form.get('email')
        matrikelnummer = request.form.get('matrikelnummer')
        studiengang_id = request.form.get('studiengang')
        student.edit_student(self=student, vorname=vorname, nachname=nachname, nds=nds, email=email,
                             matrikelnummer=matrikelnummer, studiengang_id=studiengang_id)
        return redirect(url_for('bp_mitarbeiter.admin'))

    return render_template('forms/student_form.html', student=student, arten=arten, studiengaenge=studiengaenge,
                           selected_arten=selected_arten, all_priorities=all_priorities)


# route for editing student priorities
@bp_mitarbeiter.route('/edit_priorities/<int:stud_id>', methods=['GET', 'POST'])
@login_required
@superuser_required
def edit_priorities(stud_id):
    student = Student.query.get_or_404(stud_id)
    arten = Art.query.all()
    selected_arten = [art.art_id for art in student.get_selected_arten()]
    all_priorities = Wahl.get_all_priorities(student_id=student.stud_id)
    projekte = Projekt.query.all()

    if request.method == 'POST':
        # 3 different opportunities for submission of the form
        if 'add_art' in request.form:
            to_add = int(request.form['add_art'])
            student.add_arten([to_add])
            return redirect(request.url)

        if 'remove_art' in request.form:
            to_remove = int(request.form['remove_art'])
            student.remove_art(to_remove)
            return redirect(request.url)

        if 'save_priorities' in request.form:
            art_to_save = int(request.form['save_priorities'])
            priorities = {
                1: request.form.get(f'prio{art_to_save}1'),
                2: request.form.get(f'prio{art_to_save}2'),
                3: request.form.get(f'prio{art_to_save}3')
            }

            Wahl.save_priorities(student_id=student.stud_id, art_id=art_to_save, priorities=priorities)
            return redirect(request.url)

    return render_template('forms/priorities_form.html', student=student, arten=arten, selected_arten=selected_arten,
                           all_priorities=all_priorities, projekte=projekte)


# route for deleting a student
@bp_mitarbeiter.route('/delete_student/<int:stud_id>', methods=['GET', 'POST'])
@login_required
@superuser_required
def delete_student(stud_id):
    student = Student.query.get_or_404(stud_id)

    if request.method == 'POST':
        if 'confirm' in request.form:
            student.delete_student()
        return redirect(url_for('bp_mitarbeiter.admin'))

    return render_template('forms/confirm_delete.html', student=student)


# route for adding phases
@bp_mitarbeiter.route('/add_phasen', methods=['GET', 'POST'])
@login_required
@superuser_required
def add_phasen():
    if request.method == 'POST':
        semester = request.form['semester']
        jahr = request.form['jahr']
        start_p1 = request.form['start_p1']
        ende_p1 = request.form['ende_p1']
        start_p2 = request.form['start_p2']
        ende_p2 = request.form['ende_p2']
        start_p3 = request.form['start_p3']
        ende_p3 = request.form['ende_p3']
        start_vorstellung = request.form['start_vorstellung']
        ende_vorstellung = request.form['ende_vorstellung']

        Phase.create_phasen(
            semester=semester,
            jahr=jahr,
            start_p1=start_p1,
            ende_p1=ende_p1,
            start_p2=start_p2,
            ende_p2=ende_p2,
            start_p3=start_p3,
            ende_p3=ende_p3,
            start_vorstellung=start_vorstellung,
            ende_vorstellung=ende_vorstellung
        )
        return redirect(url_for('bp_mitarbeiter.admin'))

    return render_template('forms/phasen_form.html')


# route for editing the time of the phases
@bp_mitarbeiter.route('/edit_phasen', methods=['GET', 'POST'])
@login_required
@superuser_required
def edit_phasen():
    phasen = Phase.get_current()

    if request.method == 'POST':
        start_p1 = request.form['start_p1']
        ende_p1 = request.form['ende_p1']
        start_p2 = request.form['start_p2']
        ende_p2 = request.form['ende_p2']
        start_p3 = request.form['start_p3']
        ende_p3 = request.form['ende_p3']
        start_vorstellung = request.form['start_vorstellung']
        ende_vorstellung = request.form['ende_vorstellung']

        phasen.edit_phasen(
            start_p1=start_p1,
            ende_p1=ende_p1,
            start_p2=start_p2,
            ende_p2=ende_p2,
            start_p3=start_p3,
            ende_p3=ende_p3,
            start_vorstellung=start_vorstellung,
            ende_vorstellung=ende_vorstellung
        )
        return redirect(url_for('bp_mitarbeiter.admin'))

    return render_template('forms/phasen_form.html', phasen=phasen)


# route when a new semester is started and the phase information for the current semester get deleted
@bp_mitarbeiter.route('/delete_phasen', methods=['GET', 'POST'])
@login_required
@superuser_required
def delete_phasen():
    phasen = Phase.get_current()

    if request.method == 'POST':
        if 'confirm' in request.form:
            phasen.delete_phasen()
            # Projekt.mark_all_as_old()
            # Student.delete_all_students()
        return redirect(url_for('bp_mitarbeiter.admin'))

    return render_template('forms/confirm_delete.html', phasen=phasen)
