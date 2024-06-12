from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
import ldap
from app import db
import logging
from app.models import Mitarbeiter, Student, Studiengang, StudentArt, Art, User

bp_auth = Blueprint("bp_auth", __name__, url_prefix="/auth")

loginManager = LoginManager()
loginManager.login_view = "bp_auth.login"


#logging.basicConfig(level=logging.DEBUG)




@bp_auth.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    studiengaenge = Studiengang.get_all_studiengaenge()


    # Überprüfung, ob Student bereits registriert
    student = Student.get_student(current_user.nds)

    if student:
        arten = student.get_selected_arten()
        return render_template('auth/already_registered.html',
                               student=student,
                               arten=arten)

    if request.method == 'POST':
        matrikelnummer = request.form.get('matrikelnummer')
        studiengang_id = request.form.get('studiengang')

        if not studiengang_id:
            flash('Bitte wählen Sie einen Studiengang aus.')
            return redirect(url_for('bp_auth.register'))

        student = Student.create_student(
            vorname=current_user.vorname,
            nachname=current_user.nachname,
            nds=current_user.nds,
            email=current_user.mail,
            matrikelnummer=matrikelnummer,
            studiengang_id=studiengang_id
        )

        arten_ids = request.form.getlist('arten')
        student.add_arten(arten_ids)

        arten = student.get_selected_arten()
        return render_template('auth/already_registered.html',
                               student=student,
                               arten=arten)

    return render_template('auth/register.html',
                           current_user=current_user,
                           studiengaenge=studiengaenge)

@loginManager.user_loader
def load_user(nds):
    #logging.debug(f"Loading user with NDS: {nds}")
    user_data = extendNewUser(User(nds, "", "", ""))
    return User(nds, user_data.vorname, user_data.nachname, user_data.mail)


@bp_auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nds = request.form.get('nds')
        password = request.form.get('psw')
        #logging.debug(f"Attempting to log in user: {nds}")
        if checkPasswordOfNDS(nds, password):
            user = User(nds, "", "", "")
            login_user(user)
            return redirect(url_for('bp_index.index'))
        else:
            #logging.debug(f"Invalid NDS or password for user: {nds}")
            flash("NDS oder Passwort nicht korrekt", "login")
    return render_template("auth/login.html")


@bp_auth.route("/logout")
@login_required
def logout():
    logout_user()
    if not current_user.is_authenticated:
        redirect(url_for('bp_index.index'))
    return render_template("auth/logout.html")


# LDAP FUNCTIONS
def getDN(nds):
    try:
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        connection = ldap.initialize("ldaps://ldapclient.uni-regensburg.de:636")
        connection.simple_bind_s("o=uni-regensburg,c=de")
        res = connection.search_s("o=uni-regensburg,c=de", ldap.SCOPE_SUBTREE, '(uid=' + nds + ')')
        for dn, entry in res:
            return dn
    except Exception as error:
        logging.error(f"Error in getDN: {error}")
        return None


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


def checkPasswordOfNDS(nds, password):
    dn = getDN(nds)
    if (dn == None):
        logging.debug(f"No DN found for NDS {nds}")
        return False
    return (checkPassword(dn, password))


def extendNewUser(user):
    try:
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        connection = ldap.initialize("ldaps://ldapclient.uni-regensburg.de:636")
        connection.simple_bind_s("o=uni-regensburg,c=de")
        res = connection.search_s("o=uni-regensburg,c=de", ldap.SCOPE_SUBTREE, '(uid=' + user.nds + ')')
        for dn, entry in res:
            user.vorname = entry['urrzGivenName'][0].decode('utf-8')
            user.nachname = entry['urrzSurname'][0].decode('utf-8')
            user.mail = entry['mail'][0].decode('utf-8')
            #logging.debug(f"Extended user data for NDS {user.nds}: {user.vorname} {user.nachname} {user.mail}")
            return user
    except Exception as error:
        #logging.error(f"Error in extendNewUser: {error}")
        user.vorname = "UNBEKANNT"
        user.nachname = "UNBEKANNT"
        user.mail = "UNBEKANNT"
        return user


