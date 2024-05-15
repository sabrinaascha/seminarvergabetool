from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from app.models import db
from urllib.parse import quote_plus

app = Flask(__name__)



# Datenbank-Konfiguration
db_user = 'root'
db_password = '2024'
db_coded_password = quote_plus(db_password)
db_host = 'localhost'
db_database = 'seminarvergabetool'

# SQLAlchemy Datenbank URI konfigurieren
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_user}:{db_coded_password}@{db_host}/{db_database}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Um zusätzliche Warnungen zu vermeiden

# Sicherheitsschlüssel für Sessions und Cookies
#app.config["SECRET_KEY"] = "DeinGeheimerSchlüssel"  # Ersetze dies durch einen tatsächlichen geheimen Schlüssel


# Initialisiere SQLAlchemy mit der Flask-Anwendung --> creation in models.py
#db = SQLAlchemy(app)


#blueprints importieren + registrieren
from app.views.index import bp_index
from app.views.info import bp_info
from app.views.admin import bp_admin
from app.views.auth import bp_auth

app.register_blueprint(bp_index, url_prefix="")
app.register_blueprint(bp_info, url_prefix="/info")
app.register_blueprint(bp_admin, url_prefix="/admin")
app.register_blueprint(bp_auth, url_prefix="/auth")



