from flask import Blueprint, render_template, session, request
from flask_login import current_user

from app.models import Phase, Projekt, Art

# definition of the index blueprint
bp_index = Blueprint("bp_index", __name__)

# route for the home page
@bp_index.route("/")
def index():
    # get the current phases and check which phase is active
    phasen = Phase.get_current()
    phase1_active = phasen.p1_active() if phasen else False
    phase2_active = phasen.p2_active() if phasen else False
    phase3_active = phasen.p3_active() if phasen else False

    session['is_admin'] = False  # reset admin status in the session when starting the web-application
    return render_template("index.html",
                           phasen=phasen,
                           phase1_active=phase1_active,
                           phase2_active=phase2_active,
                           phase3_active=phase3_active,
                           current_user=current_user)

# route for the rules page
@bp_index.route("/regeln")
def regeln():
    return render_template("info/regeln.html")

# route for the impressum (imprint) page
@bp_index.route("/impressum")
def impressum():
    return render_template("info/impressum.html")

# route for the data privacy page
@bp_index.route("/datenschutz")
def datenschutz():
    return render_template("info/datenschutz.html")

# route for the topics overview, with optional filtering by type
@bp_index.route('/themen', defaults={'art_filter': None}, methods=['GET'])
@bp_index.route('/<art_filter>', methods=['GET'])
def themen(art_filter):
    search_query = request.args.get('search', '')
    art_filter = art_filter  # get the type filter from the URL if selected

    valid = [art.art_typ for art in Art.get_all_arten()]
    if art_filter is not None and art_filter not in valid:
        return render_template("error/404.html"), 404  # return 404 if the type filter is invalid

    # get projects filtered by search query and type
    projekte = Projekt.get_projects_by(search_query, art_filter)
    projekte = Projekt.order_ascending_by_name(projekte)
    lehrstuhl_dict = Projekt.group_by_lehrstuhl(projekte)  # group projects by chair


    return render_template("info/themen.html",
                           lehrstuhl_dict=lehrstuhl_dict,
                           search_query=search_query,
                           arten=Art.get_all_arten(),
                           art_filter=art_filter)

# route for restricted access errors (used in decorator: within_xy_period)
@bp_index.route("/restricted")
def restricted():
    return render_template("error/out_of_period.html")

# route for unauthorized access errors (used in decorator: superuser required or mitarbeiter required)
@bp_index.route("/no_authorisation")
def no_authorisation():
    return render_template("error/not_authorized.html")
