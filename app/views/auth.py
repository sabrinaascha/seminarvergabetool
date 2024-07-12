from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
import ldap
import logging
from app.models import User

# definition of the authentication blueprint
bp_auth = Blueprint("bp_auth", __name__, url_prefix="/auth")

# initialize the login manager
loginManager = LoginManager()
loginManager.login_view = "bp_auth.login"

# user loader to load user data based on the NDS identifier
@loginManager.user_loader
def load_user(nds):
    user_data = extendNewUser(User(nds, "", "", ""))
    return User(nds, user_data.vorname, user_data.nachname, user_data.mail)

# route for user login
@bp_auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nds = request.form.get('nds')
        password = request.form.get('psw')
        if checkPasswordOfNDS(nds, password):
            user = User(nds, "", "", "")
            login_user(user)
            return redirect(url_for('bp_index.index'))
        else:
            flash("NDS or password incorrect", "login")
    return render_template("auth/login.html")

# route for user logout
@bp_auth.route("/logout")
@login_required
def logout():
    logout_user()
    if not current_user.is_authenticated:
        redirect(url_for('bp_index.index'))
    return render_template("auth/logout.html")


# retrieve the Distinguished Name (DN) for a user based on the nds
def getDN(nds):
    try:
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        connection = ldap.initialize("ldaps://ldapclient.uni-regensburg.de:636")
        connection.simple_bind_s("o=uni-regensburg,c=de")
        res = connection.search_s("o=uni-regensburg,c=de", ldap.SCOPE_SUBTREE, f'(uid={nds})')
        for dn, entry in res:
            return dn
    except Exception as error:
        logging.error(f"Error in getDN: {error}")
        return None

# check the password for a given DN (Distinguished Name)
def checkPassword(dn, password):
    try:
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
        ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, "etc/ssl/certs/RootCAA.pem")
        connection = ldap.initialize("ldaps://ldapclient.uni-regensburg.de:636")
        connection.simple_bind_s(dn, password)
        return True
    except Exception as error:
        logging.error(f"Error in checkPassword: {error}")
        return False

# verify the if nds and pw is correct
def checkPasswordOfNDS(nds, password):
    dn = getDN(nds)
    if dn is None:
        return False
    return checkPassword(dn, password)

# extend the user object with additional attributes (first name, last name, email) from the LDAP directory
def extendNewUser(user):
    try:
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        connection = ldap.initialize("ldaps://ldapclient.uni-regensburg.de:636")
        connection.simple_bind_s("o=uni-regensburg,c=de")
        res = connection.search_s("o=uni-regensburg,c=de", ldap.SCOPE_SUBTREE, f'(uid={user.nds})')
        for dn, entry in res:
            user.vorname = entry['urrzGivenName'][0].decode('utf-8')
            user.nachname = entry['urrzSurname'][0].decode('utf-8')
            user.mail = entry['mail'][0].decode('utf-8')
            return user
    except Exception as error:
        user.vorname = "UNKNOWN"
        user.nachname = "UNKNOWN"
        user.mail = "UNKNOWN"
        return user
