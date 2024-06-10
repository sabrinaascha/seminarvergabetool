from flask import Blueprint, render_template, request
from flask_login import current_user
from app.models import Projekt, ProjektMitarbeiter, Art, Lehrstuhl, Mitarbeiter, Fach, Student
from app import app, db, helper

bp_themen = Blueprint("bp_themen", __name__)

@bp_themen.route("/")
def themen():
    search_query = request.args.get('search', '')
    art_filter = request.args.get('art_typ', '')

    projekte = get_projects(search_query, art_filter)
    lehrstuhl_dict = group_by_lehrstuhl(projekte)

    return render_template("themen/themen.html",
                           lehrstuhl_dict=lehrstuhl_dict,
                           search_query=search_query,
                           arten=Art.get_art_typen(),
                           art_filter=art_filter)


@bp_themen.route('/<art_typ>')
def themen_by_art(art_typ):
    projekte = get_projects(art_filter=art_typ)
    lehrstuhl_dict = group_by_lehrstuhl(projekte)

    return render_template("themen/themen_by_art.html",
                           art_typ=art_typ,
                           lehrstuhl_dict=lehrstuhl_dict)


@bp_themen.route('/wahl')
def themenwahl():
    projekte = Projekt.query.all()  # Annahme: Projekt ist das Modell für Themen
    return render_template('themen/themenwahl.html',
                           projekte=projekte)


def submit_themenwahl():
    return None


def get_projects(search_query=None, art_filter=None):
    projekte = Projekt.query
    if search_query:
        projekte = apply_keyword_search(projekte, search_query)
    if art_filter:
        projekte = projekte.join(Projekt.art).filter(Art.art_typ == art_filter)
    return projekte.all()

def group_by_lehrstuhl(projekte):
    lehrstuhl_dict = {}
    for projekt in projekte:
        lehrstuhl_name = projekt.lehrstuhl.name
        if lehrstuhl_name not in lehrstuhl_dict:
            lehrstuhl_dict[lehrstuhl_name] = []
        lehrstuhl_dict[lehrstuhl_name].append(projekt)
    return lehrstuhl_dict


def apply_keyword_search(query, search_query):
    if search_query:
        search_filter = f"%{search_query}%"
        query = query.filter(
            (Projekt.titel.ilike(search_filter)) |
            (Projekt.beschreibung.ilike(search_filter)) |
            (Fach.bezeichnung.ilike(search_filter)) |
            (Art.art_typ.ilike(search_filter)) |
            (Projekt.betreuer.any(Mitarbeiter.vorname.ilike(search_query))) |
            (Projekt.betreuer.any(Mitarbeiter.nachname.ilike(search_query)))
        )
    return query




