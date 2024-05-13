from flask import Blueprint, render_template, jsonify


# BLUEPRINT "bp_index"
bp_index = Blueprint("bp_index", __name__)


@bp_index.route("/")
def index():
    html = Html.get_html()
    aktuell = html.aktuell
    headline = html.headline
    oeffnungszeiten = html.text
    return render_template(
        "index/base.html",
        aktuell=aktuell,
        headline=headline,
        oeffnungszeiten=oeffnungszeiten,
    )
