from flask import Flask
from urllib.parse import quote_plus

# app initialization
app = Flask(__name__)

from app.helper import datetime_local
from app.models import db
from app.views.auth import loginManager

# database configuration
db_user = 'root'
db_password = '2024'
db_coded_password = quote_plus(db_password)  # encoding of the database password
db_host = 'localhost'
db_database = 'seminarvergabetool'

# configuration of sql alchemy database u
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{db_user}:{db_coded_password}@{db_host}/{db_database}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "psc9BNcMna6mQx41zNILLaYY4xlTVXIJ" # secret key for session management and security


# initialize database (instantiation of db-object in models.py)
db.init_app(app)
with app.app_context():
    db.create_all() # creates all database tables based on model.py


# initialize login manager (instantiation in auth.py)
loginManager.init_app(app)

# import of the blueprints
from app.views.index import bp_index
from app.views.auth import bp_auth
from app.views.mitarbeiter import bp_mitarbeiter
from app.views.student import bp_student

# registering the blueprints with their url_prefix
app.register_blueprint(bp_index, url_prefix="")
app.register_blueprint(bp_auth, url_prefix="/auth")
app.register_blueprint(bp_mitarbeiter, url_prefix="/mitarbeiter")
app.register_blueprint(bp_student, url_prefix="/student")

# registers jinja-template filter datetime_local (function in helper.py)
app.jinja_env.filters['datetime_local'] = datetime_local
