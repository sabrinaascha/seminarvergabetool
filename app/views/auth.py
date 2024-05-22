from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
import ldap
from app.models import Mitarbeiter, Student

bp_auth = Blueprint("bp_auth", __name__, url_prefix="/auth")

loginManager = LoginManager()
loginManager.login_view = "bp_auth.login"


class User(UserMixin):
    def __init__(self, nds, vorname, nachname, mail, ):
        self.nds = nds
        self.vorname = vorname
        self.nachname = nachname
        self.mail = mail

    def get_id(self):
        return self.nds

@loginManager.user_loader
def load_user(nds):
    #user_data = extendNewUser(User(nds,"","",""))
    return Mitarbeiter.query.filter_by(nds=nds).first()  #User(nds,user_data.vorname,user_data.nachname,user_data.mail)

@bp_auth.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        nds = request.form.get('nds')
        password = request.form.get('psw')
        if checkPasswordOfNDS(nds, password):
            user = load_user(nds)  #User(nds,"","","")
            login_user(user)
            return redirect(url_for('bp_index.index'))
        else:
            flash("NDS oder Passwort nicht korrekt", "login")
    return render_template("auth/login.html")

@bp_auth.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("auth/logout.html")


#ldap SPÄTER!
def checkPasswordOfNDS(nds, password):
    return True
'''
dn = getDN(nds)
if(dn == None):
return False
return(checkPassword(dn, password))
'''

