from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from app.models import Projekt, ProjektBetreuer, Art, Lehrstuhl, Mitarbeiter, Fach
from app import app, db, helper

bp_profil = Blueprint("bp_profile", __name__)


@bp_profil.route("/profil")
#@login_required
def profile():


    return render_template(
        "profil/mitarbeiter.html",
        studentName=studentData[0],
        studentPrivateData=studentData[1:],
        lockerNumber=lockerData[0],
        lockerInformation=lockerData[1:],
        studentHasReservationVis=hasReservationVis,
        studentHasNoReservationVis=hasNoReservationVis,
        is_mitarbeiter=is_mitarbeiter,  # Übergeben des Flag für Mitarbeiterstatus an die Vorlage
        mitarbeiter=mitarbeiter,
        alle_mitarbeiter=alle_mitarbeiter
    )

def mitarbeiter():
    is_mitarbeiter = Mitarbeiter.query.filter_by(nds=current_user.nds).first() is not None
    mitarbeiter = None
    alle_mitarbeiter = None

    if is_mitarbeiter:
        mitarbeiter, lehrstuhl = get_mitarbeiter(current_user.nds)
        lehrstuhl = Lehrstuhl.query.get(mitarbeiter.Lehrstuhl_lehrstuhl_id)
        alle_mitarbeiter = Mitarbeiter.query.filter_by(Lehrstuhl_lehrstuhl_id=lehrstuhl.lehrstuhl_id).all()