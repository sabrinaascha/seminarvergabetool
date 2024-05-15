from flask import Blueprint, render_template


bp_admin = Blueprint("bp_admin", __name__, url_prefix="/admin")

@bp_admin.route("/")
#@login_required
#@superuser_required
def admin():
    return render_template(
        "admin/admin.html"
        )