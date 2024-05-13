from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta

db = SQLAlchemy()


# Tables
class Art(db.Model):
    art_id = db.Column(db.Integer, primary_key=True)
    art_typ = db.Column(db.String(50))


class Projekt(db.Model):
    __tablename__ = 'projekt'
    projekt_id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(100))
    beschreibung = db.Column(db.String(200))
    max_anzahl = db.Column(db.Integer)
    studiengang = db.Column(db.Integer)
    fach = db.Column(db.Integer)
    semester = db.Column(db.Integer)
    neu = db.Column(db.Integer)
    Art_art_id = db.Column(db.Integer, db.ForeignKey('art.art_id'), nullable=False)
    Lehrstuhl_lehrstuhl_id = db.Column(db.Integer, db.ForeignKey('lehrstuhl.lehrstuhl_id'), nullable=False)

    art = db.relationship('Art', backref=db.backref('projekt', lazy=True))
    lehrstuhl = db.relationship('Lehrstuhl', backref=db.backref('projekt', lazy=True))

    betreuer = db.relationship('Projekt_Betreuer', backref=db.backref('projekt', lazy='subquery'))
    #aufgrund n:m Verknüfung sowohl bei Mitarbeiter als auch Projekt
    betreute_projekte = db.relationship('Projekt_Betreuer', backref='projekt', lazy=True)

    def __init__(self, titel, beschreibung, max_anzahl, studiengang, fach, semester, neu, Art_art_id, Lehrstuhl_lehrstuhl_id):
        self.titel = titel
        self.beschreibung = beschreibung
        self.max_anzahl = max_anzahl
        self.studiengang = studiengang
        self.fach = fach
        self.semester = semester
        self.neu = neu
        self.Art_art_id = Art_art_id
        self.Lehrstuhl_lehrstuhl_id = Lehrstuhl_lehrstuhl_id


    def show_all_values(self):
        return Projekt

    def get_all_projekte():
        query = Projekt.query
        return query

    @staticmethod
    def get_projekte_by_lehrstuhl(lehrstuhl_id):
        return Projekt.query.filter_by(Lehrstuhl_lehrstuhl_id=lehrstuhl_id).all()


class Lehrstuhl(db.Model):
    __tablename__ = 'lehrstuhl'

    lehrstuhl_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    homepage = db.Column(db.String(50))

    def __init__(self, name, homepage):
        self.name = name
        self.homepage = homepage


class Mitarbeiter(db.Model):
    __tablename__ = 'mitarbeiter'

    ma_id = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(20))
    nachname = db.Column(db.String(20))
    nds = db.Column(db.String(10))
    email = db.Column(db.String(30))
    rolle = db.Column(db.Integer)
    Lehrstuhl_lehrstuhl_id = db.Column(db.Integer, db.ForeignKey('lehrstuhl.lehrstuhl_id'), nullable=False)
    lehrstuhl = db.relationship('Lehrstuhl', backref=db.backref('mitarbeiter', lazy=True))

    betreute_projekte = db.relationship('Projekt_Betreuer', backref=db.backref('betreuer', lazy='subquery'))

    def __init__(self, vorname, nachname, nds, email, rolle, Lehrstuhl_lehrstuhl_id):
        self.vorname = vorname
        self.nachname = nachname
        self.nds = nds
        self.email = email
        self.rolle = rolle
        self.Lehrstuhl_lehrstuhl_id = Lehrstuhl_lehrstuhl_id

    @staticmethod
    def get_all_Mitarbeiter():
        return Mitarbeiter.query.all()

    def get_mitarbeiter(nds=""):
        if nds != "":
            mitarbeiter = Mitarbeiter.query.filter_by(nds=nds).first()
        return mitarbeiter

    def get_all_nds():
        query = Mitarbeiter.query.filter(Mitarbeiter.nds != "0").all()
        all_nds = []
        for entry in query:
            all_nds.append(entry.nds)
        return all_nds


class Projekt_Betreuer(db.Model):
    __tablename__ = 'projekt_betreuer'
    pb_id = db.Column(db.Integer, primary_key=True)
    Mitarbeiter_ma_id = db.Column(db.Integer, db.ForeignKey('mitarbeiter.ma_id'))
    Projekt_projekt_id = db.Column(db.Integer, db.ForeignKey('projekt.projekt_id'))

    __table_args__ = {'extend_existing': True}

    @staticmethod
    def get_all_projekt_betreuer():
        betreuer = Projekt_Betreuer.query.all()
        return betreuer