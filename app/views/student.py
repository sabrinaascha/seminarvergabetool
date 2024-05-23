from flask import Blueprint, render_template, request
from app.models import Projekt, ProjektBetreuer, Art, Lehrstuhl, Mitarbeiter, Fach
from app import app, db

bp_student = Blueprint("bp_student", __name__)

@bp_student.route("/themensuche")
def themensuche():
    # wenn zeit < start_p2 --> render_template("error/not_available.html", start_p2)

    search_query = request.args.get('search', '')

    # Base query to fetch all projects with their related data
    query = db.session.query(Projekt, Lehrstuhl, Art, Fach).join(Lehrstuhl,
                                                                 Projekt.lehrstuhl_lehrstuhl_id == Lehrstuhl.lehrstuhl_id) \
        .join(Art, Projekt.art_art_id == Art.art_id) \
        .join(Fach, Projekt.fach_fach_id == Fach.fach_id)

    # If there is a search query, filter the projects based on the search keyword
    if search_query:
        search_filter = f"%{search_query}%"
        query = query.filter(
            (Projekt.titel.ilike(search_filter)) |
            (Projekt.beschreibung.ilike(search_filter)) |
            (Fach.bezeichnung.ilike(search_filter)) |
            (Art.art_typ.ilike(search_filter))
        )

    # Execute the query and fetch results
    projects = query.all()

    # Group projects by Lehrstuhl
    lehrstuhl_dict = {}
    for project, lehrstuhl, art, fach in projects:
        if lehrstuhl.name not in lehrstuhl_dict:
            lehrstuhl_dict[lehrstuhl.name] = []

        betreuer = db.session.query(Mitarbeiter).join(ProjektBetreuer,
                                                       Mitarbeiter.ma_id == ProjektBetreuer.mitarbeiter_ma_id).filter(
            ProjektBetreuer.projekt_projekt_id == project.projekt_id).all()

        project_data = {
            'project': project, #listen
            'art': art,
            'fach': fach,
            'betreuer': betreuer
        }
        lehrstuhl_dict[lehrstuhl.name].append(project_data)

    return render_template("student/themensuche.html", lehrstuhl_dict=lehrstuhl_dict)