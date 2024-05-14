from flask import Blueprint, render_template


# BLUEPRINT "bp_index"
bp_index = Blueprint("bp_index", __name__)


@bp_index.route("/")
def index():
    return render_template("index.html")

# BLUEPRINT "bp_info"
bp_info = Blueprint("bp_info", __name__)

@bp_info.route("/")
def info():
    return render_template("info/info.html")

@bp_info.route("/impressum")
def impressum():
    return render_template("info/impressum.html")

@bp_info.route("/agb")
def agb():
    return render_template("info/agb.html")


