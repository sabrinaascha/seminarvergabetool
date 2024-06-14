from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import current_user, login_required

from app.models import Projekt, ProjektMitarbeiter, Art, Lehrstuhl, Mitarbeiter, Fach, Studiengang
from app import app, db, helper

bp_mitarbeiter = Blueprint("bp_mitarbeiter", __name__)


@bp_mitarbeiter.route("/")
@login_required
def profil():
    mitarbeiter = Mitarbeiter.get_mitarbeiter(current_user.nds)
    projekte = mitarbeiter.lehrstuhl.get_lehrstuhl_projekte()
    return render_template("mitarbeiter/profil.html",
                           mitarbeiter=mitarbeiter,
                           projekte=projekte
                           )


@bp_mitarbeiter.route('/thema_einstellen', methods=['GET', 'POST'])
@login_required
def add_projekt():
    arten = Art.get_all_arten()
    studiengaenge = Studiengang.get_all_studiengaenge()
    faecher= Fach.get_all_faecher()

    mitarbeiter = Mitarbeiter.get_mitarbeiter(current_user.nds)



    if request.method == 'POST':
        titel = request.form.get('titel')
        beschreibung = request.form.get('beschreibung')
        max_anzahl = request.form.get('max_anzahl')
        studiengang_id = request.form.get('studiengang')
        art_id = request.form.get('art')
        fach_id = request.form.get('fach')
        betreuer_ids = request.form.getlist('betreuer')


        projekt = Projekt.create_projekt(
            titel=titel,
            beschreibung=beschreibung,
            max_anzahl=max_anzahl,
            studiengang_id=studiengang_id,
            fach_id=fach_id,
            lehrstuhl_id=mitarbeiter.lehrstuhl_lehrstuhl_id,
            art_id=art_id,
            betreuer_ids=betreuer_ids
        )

        return redirect(url_for('bp_mitarbeiter.profil'))

    return render_template('mitarbeiter/projekt_form.html',
                           mitarbeiter=mitarbeiter,
                           studiengaenge=studiengaenge,
                           arten=arten,
                           faecher=faecher)


@login_required
@bp_mitarbeiter.route('/edit/<int:projekt_id>', methods=['GET', 'POST'])
def edit_projekt(projekt_id):
    mitarbeiter = Mitarbeiter.get_mitarbeiter(current_user.nds)
    
    projekt = Projekt.query.get(projekt_id)

    studiengaenge = Studiengang.get_all_studiengaenge()
    arten = Art.get_all_arten()
    faecher = Fach.get_all_faecher()

    if request.method == 'POST':
        titel = request.form.get('titel')
        beschreibung = request.form.get('beschreibung')
        max_anzahl = request.form.get('max_anzahl')
        studiengang_id = request.form.get('studiengang')
        art_id = request.form.get('art')
        betreuer_ids = request.form.getlist('betreuer')

        projekt.edit_projekt(titel, beschreibung, max_anzahl, studiengang_id, art_id, betreuer_ids)

        flash('Das Projekt wurde erfolgreich bearbeitet.', 'success')
        return redirect(url_for('bp_mitarbeiter.profil'))

    return render_template('mitarbeiter/projekt_form.html',
                           projekt=projekt,
                           mitarbeiter=mitarbeiter,
                           studiengaenge=studiengaenge,
                           arten=arten,
                           faecher=faecher)


@bp_mitarbeiter.route('/delete/<int:projekt_id>', methods=['GET', 'POST'])
@login_required
def delete(projekt_id):
    projekt = Projekt.query.get_or_404(projekt_id)
    if request.method == 'POST':
        if 'confirm' in request.form:
            projekt.delete_projekt()
            flash('Das Projekt wurde erfolgreich gelöscht.', 'success')
        return redirect(url_for('bp_mitarbeiter.profil'))

    return render_template('mitarbeiter/confirm_delete_project.html', projekt=projekt)

@bp_mitarbeiter.route('/mitarbeiter_hinzufuegen', methods=['GET', 'POST'])
@login_required
def add_betreuer():
    mitarbeiter = Mitarbeiter.get_mitarbeiter(current_user.nds)

    if request.method == 'POST':
        vorname = request.form.get('vorname')
        nachname = request.form.get('nachname')
        nds = request.form.get('nds')
        email = request.form.get('email')


        mitarbeiter = Mitarbeiter.create_mitarbeiter(
            vorname=vorname,
            nachname=nachname,
            nds=nds,
            email=email,
            lehrstuhl_id=mitarbeiter.lehrstuhl_lehrstuhl_id
        )
        flash("Betreuer erfolgreich hinzugefügt", "success")
        return redirect(url_for('bp_mitarbeiter.profil'))

    return render_template('mitarbeiter/mitarbeiter_hinzufuegen.html',
                           mitarbeiter=mitarbeiter)