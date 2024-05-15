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

class Student(db.Model):
    __tablename__ = 'student'

    stud_id = db.Column(db.Integer, primary_key=True)
    nachname = db.Column(db.String(20))
    vorname = db.Column(db.String(20))
    nds = db.Column(db.String(10))
    email = db.Column(db.String(20))
    matrikel = db.Column(db.Integer)
    studiengang = db.Column(db.Integer)
    gruppe_status = db.Column(db.Integer)
    trm_number = db.Column(db.Integer)
    Gruppe_gruppe_id = db.Column(db.Integer, db.ForeignKey('gruppe.gruppe_id'))

    gruppe = db.relationship('Gruppe', backref=db.backref('studenten', lazy=True))
    student_art = db.relationship('Student_Art', backref='student', lazy=True)

    def __init__(self, nachname, vorname, nds, email, matrikel, studiengang, gruppe_status, trm_number,
                 Gruppe_gruppe_id):
        self.nachname = nachname
        self.vorname = vorname
        self.nds = nds
        self.email = email
        self.matrikel = matrikel
        self.studiengang = studiengang
        self.gruppe_status = gruppe_status
        self.trm_number = trm_number
        self.Gruppe_gruppe_id = Gruppe_gruppe_id

class Student_Art(db.Model):
    __tablename__ = 'student_art'

    stud_art_id = db.Column(db.Integer, primary_key=True)
    Art_art_id = db.Column(db.Integer, db.ForeignKey('art.art_id'))
    Student_stud_id = db.Column(db.Integer, db.ForeignKey('student.stud_id'))

    art = db.relationship('Art', backref=db.backref('student_arts', lazy=True))

    def __init__(self, Art_art_id, Student_stud_id):
        self.Art_art_id = Art_art_id
        self.Student_stud_id = Student_stud_id

class Phase(db.Model):
    __tablename__ = 'phase'

    semester_id = db.Column(db.Integer, primary_key=True)
    semester = db.Column(db.String(20), nullable=False)
    registrierung_start = db.Column(db.DateTime, nullable=False)
    registrierung_ende = db.Column(db.DateTime, nullable=False)
    wahl_start = db.Column(db.DateTime, nullable=False)
    wahl_ende = db.Column(db.DateTime, nullable=False)
    vergabe_start = db.Column(db.DateTime, nullable=False)
    vergabe_ende = db.Column(db.DateTime, nullable=False)

    def __init__(self, semester_id, semester, registrierung_start, registrierung_ende, wahl_start, wahl_ende,
                 vergabe_start, vergabe_ende):
        self.semester_id = semester_id
        self.semester = semester
        self.registrierung_start = registrierung_start
        self.registrierung_ende = registrierung_ende
        self.wahl_start = wahl_start
        self.wahl_ende = wahl_ende
        self.vergabe_start = vergabe_start
        self.vergabe_ende = vergabe_ende


class Superusers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nds = db.Column(db.String(8))

    def get_all_superusers():
        query = Superusers.query.filter().all()
        all_users = []
        for entry in query:
            all_users.append(entry.nds)
        return all_users