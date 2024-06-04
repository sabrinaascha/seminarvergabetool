from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from app.models import db
from app.views.auth import loginManager
from urllib.parse import quote_plus

#app initialization
app = Flask(__name__)



# Datenbase configuration
db_user = 'root'
db_password = '2024'
db_coded_password = quote_plus(db_password)
db_host = 'localhost'
db_database = 'seminarvergabetool'

# SQLAlchemy Datenbank URI konfigurieren
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{db_user}:{db_coded_password}@{db_host}/{db_database}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Um zusätzliche Warnungen zu vermeiden
app.config["SECRET_KEY"] = "psc9BNcMna6mQx41zNILLaYY4xlTVXIJ"


# initialize database, get's created in models.py
db.init_app(app)
with app.app_context():  # throws error without 'app.app_context():'
    db.create_all()

# AUTHENTICATION
# initialize login manager, get's created in auth.py
loginManager.init_app(app)

#blueprints importieren + registrieren
from app.views.index import bp_index
from app.views.info import bp_info
from app.views.admin import bp_admin
from app.views.auth import bp_auth
from app.views.themen import bp_themen
from app.views.profil import bp_profil

app.register_blueprint(bp_index, url_prefix="")
app.register_blueprint(bp_info, url_prefix="/info")
app.register_blueprint(bp_admin, url_prefix="/admin")
app.register_blueprint(bp_auth, url_prefix="/auth")
app.register_blueprint(bp_themen, url_prefix="/themen")
app.register_blueprint(bp_profil, url_prefix="/profil")



