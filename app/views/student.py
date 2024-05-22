from flask import Blueprint, render_template
from app.models import Projekt, ProjektBetreuer, Art, Lehrstuhl

bp_themensuche = Blueprint("bp_themensuche", __name__)

@bp_themensuche.route("/")
def themensuche():
    #wenn zeit < start_p2 --> render_template("error/not_available.html", start_p2)
    betreuer = ProjektBetreuer.get_betreuer()
    return render_template("student/themensuche.html", )