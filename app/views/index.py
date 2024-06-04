from flask import Blueprint, render_template
from flask_login import login_required

from app.models import Phase


# BLUEPRINT "bp_index"
bp_index = Blueprint("bp_index", __name__)


@bp_index.route("/")
def index():
    phasen = {
        'phase1_start': '15.01. 8:00 Uhr',
        'phase1_end': '26.01.2024 9:00 Uhr',
        'phase2_start': '26.01. 12:00 Uhr',
        'phase2_end': '31.01.2024 12:00 Uhr',
        'phase3_start': '05.02. 8:00 Uhr',
        'phase3_end': '09.02.2024 17:00 Uhr'
    }
    return render_template("index.html",
                           phasen = phasen)




