from datetime import datetime
from functools import wraps

from flask import redirect, url_for, render_template
from flask_login import current_user

from app import app
from app.models import Superuser, Phase


# used when a route is only available for admins
def superuser_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not Superuser.is_admin(current_user.nds):
            return redirect(url_for('bp_index.no_authorisation'))
        return func(*args, **kwargs)

    return decorated_view


# used  for routes in mitarbeiter.py, that students cannot access the employee functions
def mitarbeiter_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_mitarbeiter:
            return redirect(url_for('bp_index.no_authorisation'))
        return func(*args, **kwargs)

    return decorated_view


# checks if we are currently in registration phase, else routes using that decorator get blocked (restricted template)
def within_registration_period(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_phase = Phase.get_current()
        if not current_phase or not (current_phase.start_p1 <= datetime.now() <= current_phase.ende_p1):
            return redirect(url_for('bp_index.restricted'))
        return f(*args, **kwargs)

    return decorated_function


# checks if we are currently in second phase, else routes using that decorator get blocked (restricted template)
def within_prioritization_period(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_phase = Phase.get_current()
        if not current_phase or not (current_phase.start_p2 <= datetime.now() <= current_phase.ende_p2):
            return redirect(url_for('bp_index.restricted'))
        return f(*args, **kwargs)

    return decorated_function


#  formats a datetime object into a string format (necessary for "datetime-local" inputs)
def datetime_local(value):
    if value:
        return value.strftime('%Y-%m-%dT%H:%M')
    return ''


# handles the 404 error with a custom template
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404
