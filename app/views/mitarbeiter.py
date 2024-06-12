from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import current_user, login_required

from app.models import Projekt, ProjektMitarbeiter, Art, Lehrstuhl, Mitarbeiter, Fach, Studiengang
from app import app, db, helper

bp_mitarbeiter = Blueprint("bp_mitarbeiter", __name__)


@bp_mitarbeiter.route("/profil")
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
def add_thema():
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
        betreuer = request.form.getlist('betreuer')


        projekt = Projekt.create_projekt(
            titel=titel,
            beschreibung=beschreibung,
            max_anzahl=max_anzahl,
            studiengang_id=studiengang_id,
            fach_id=fach_id,
            lehrstuhl_id=mitarbeiter.lehrstuhl_lehrstuhl_id,
            art_id=art_id
        )

        for b in betreuer:
            projekt.add_projekt_betreuer(b)

        return redirect(url_for('bp_index.index'))

    return render_template('mitarbeiter/thema_einstellen.html',
                           mitarbeiter=mitarbeiter,
                           studiengaenge=studiengaenge,
                           arten=arten,
                           faecher=faecher)

def mitarbeiter():
    is_mitarbeiter = Mitarbeiter.query.filter_by(nds=current_user.nds).first() is not None
    mitarbeiter = None
    alle_mitarbeiter = None

    if is_mitarbeiter:
        mitarbeiter, lehrstuhl = Mitarbeiter.get_mitarbeiter(current_user.nds)
        lehrstuhl = Lehrstuhl.query.get(mitarbeiter.Lehrstuhl_lehrstuhl_id)
        alle_mitarbeiter = Mitarbeiter.query.filter_by(Lehrstuhl_lehrstuhl_id=lehrstuhl.lehrstuhl_id).all()