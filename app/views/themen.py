from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from app.models import Projekt, ProjektMitarbeiter, Art, Lehrstuhl, Mitarbeiter, Fach, Student, Wahl, Studiengang
from app import app, db, helper

bp_themen = Blueprint("bp_themen", __name__)

@bp_themen.route('/', methods=['GET'])
def themen():
    search_query = request.args.get('search', '')
    art_filter = request.args.get('art_typ', '')

    projekte = Projekt.get_projects_by(search_query, art_filter)
    lehrstuhl_dict = Projekt.group_by_lehrstuhl(projekte)

    return render_template("themen/themen.html",
                           lehrstuhl_dict=lehrstuhl_dict,
                           search_query=search_query,
                           arten=Art.get_all_arten(),
                           art_filter=art_filter)


@bp_themen.route('/<art_typ>')
def themen_by_art(art_typ):
    projekte = Projekt.get_projects_by(art_filter=art_typ)
    lehrstuhl_dict = Projekt.group_by_lehrstuhl(projekte)

    return render_template("themen/themen_by_art.html",
                           art_typ=art_typ,
                           lehrstuhl_dict=lehrstuhl_dict)








def submit_themenwahl():
    return None








