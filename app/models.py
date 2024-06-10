from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta

db = SQLAlchemy()


class Gruppe(db.Model):
    __tablename__ = 'gruppe'
    gruppe_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    status = db.Column(db.Boolean)


class Studiengang(db.Model):
    __tablename__ = 'studiengang'
    studiengang_id = db.Column(db.Integer, primary_key=True)
    bezeichnung = db.Column(db.String(50))
    abschluss = db.Column(db.String(10))

    @classmethod
    def get_all_studiengaenge(cls):
        return Studiengang.query.all()


class Fach(db.Model):
    __tablename__ = 'fach'
    fach_id = db.Column(db.Integer, primary_key=True)
    bezeichnung = db.Column(db.String(50))


class Art(db.Model):
    __tablename__ = 'art'
    art_id = db.Column(db.Integer, primary_key=True)
    art_typ = db.Column(db.String(30))

    students = db.relationship('Student', secondary='student_art', back_populates='arten')

    @staticmethod
    def get_art_typen():
        return Art.query.distinct(Art.art_typ).all()


class Lehrstuhl(db.Model):
    __tablename__ = 'lehrstuhl'
    lehrstuhl_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    homepage = db.Column(db.String(50))


class Rolle(db.Model):
    __tablename__ = 'rolle'
    rolle_id = db.Column(db.Integer, primary_key=True)
    bezeichnung = db.Column(db.String(20))


class Student(db.Model):
    __tablename__ = 'student'
    stud_id = db.Column(db.Integer, primary_key=True)
    nachname = db.Column(db.String(30))
    vorname = db.Column(db.String(20))
    nds = db.Column(db.String(10))
    email = db.Column(db.String(50))
    matrikelnummer = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    gruppe_gruppe_id = db.Column(db.Integer, db.ForeignKey('gruppe.gruppe_id'))
    studiengang_studiengang_id = db.Column(db.Integer, db.ForeignKey('studiengang.studiengang_id'), nullable=False)

    gruppe = db.relationship('Gruppe', backref=db.backref('students', lazy=True))
    studiengang = db.relationship('Studiengang', backref=db.backref('students', lazy=True))
    arten = db.relationship('Art', secondary='student_art', back_populates='students')


    @staticmethod
    def is_student(nds=""):
        return Student.query.filter_by(nds=nds).first() is not None

    @staticmethod
    def create_student(vorname, nachname, nds, email, matrikelnummer, studiengang_id):
        student = Student(vorname=vorname, nachname=nachname, nds=nds, email=email, matrikel=matrikelnummer,
                          studiengang_studiengang_id=studiengang_id)
        db.session.add(student)
        db.session.commit()
        return student

    @staticmethod
    def get_all_Students():
        return Student.query.all()

    def get_student(nds=""):
        if nds != "":
            student = Student.query.filter_by(nds=nds).first()
        return student

    def get_all_nds():
        query = Student.query.filter(Student.nds != "0").all()
        all_nds = []
        for entry in query:
            all_nds.append(entry.nds)
        return all_nds


class StudentArt(db.Model):
    _tablename_ = 'student_art'
    stud_art_id = db.Column(db.Integer, primary_key=True)
    art_art_id = db.Column(db.Integer, db.ForeignKey('art.art_id'))
    student_stud_id = db.Column(db.Integer, db.ForeignKey('student.stud_id'))

    #art = db.relationship('Art', backref=db.backref('student_art', lazy=True))
    #student = db.relationship('Student', backref=db.backref('student_art', lazy=True))


    @staticmethod
    def get_selected_arten(stud_id):
        return db.session.query(Art).join(StudentArt).filter(StudentArt.stud_art_id == stud_id).all()


class Mitarbeiter(db.Model):
    __tablename__ = 'mitarbeiter'
    ma_id = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(20))
    nachname = db.Column(db.String(30))
    nds = db.Column(db.String(10))
    email = db.Column(db.String(50))
    rolle_rolle_id = db.Column(db.Integer, db.ForeignKey('rolle.rolle_id'), nullable=False)
    lehrstuhl_lehrstuhl_id = db.Column(db.Integer, db.ForeignKey('lehrstuhl.lehrstuhl_id'), nullable=False)

    rolle = db.relationship('Rolle', backref=db.backref('mitarbeiter', lazy=True))
    lehrstuhl = db.relationship('Lehrstuhl', backref=db.backref('mitarbeiter', lazy=True))

    betreute_projekte = db.relationship('Projekt', secondary='projekt_mitarbeiter', back_populates='betreuer')

    @classmethod
    def mitarbeiter_exists(nds=""):
        return Mitarbeiter.query.filter_by(nds=nds).first() is not None

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


class Projekt(db.Model):
    __tablename__ = 'projekt'
    projekt_id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(100))
    beschreibung = db.Column(db.String(200))
    max_anzahl = db.Column(db.Integer)
    neu = db.Column(db.Boolean)
    studiengang_studiengang_id = db.Column(db.Integer, db.ForeignKey('studiengang.studiengang_id'), nullable=False)
    fach_fach_id = db.Column(db.Integer, db.ForeignKey('fach.fach_id'), nullable=False)
    art_art_id = db.Column(db.Integer, db.ForeignKey('art.art_id'), nullable=False)
    lehrstuhl_lehrstuhl_id = db.Column(db.Integer, db.ForeignKey('lehrstuhl.lehrstuhl_id'), nullable=False)

    studiengang = db.relationship('Studiengang', backref=db.backref('projekt', lazy=True))
    fach = db.relationship('Fach', backref=db.backref('projekt', lazy=True))
    art = db.relationship('Art', backref=db.backref('projekt', lazy=True))
    lehrstuhl = db.relationship('Lehrstuhl', backref=db.backref('projekt', lazy=True))

    betreuer = db.relationship('Mitarbeiter', secondary='projekt_mitarbeiter', back_populates='betreute_projekte')


class ProjektMitarbeiter(db.Model):
    __tablename__ = 'projekt_mitarbeiter'
    pb_id = db.Column(db.Integer, primary_key=True)
    mitarbeiter_ma_id = db.Column(db.Integer, db.ForeignKey('mitarbeiter.ma_id'), nullable=False)
    projekt_projekt_id = db.Column(db.Integer, db.ForeignKey('projekt.projekt_id'), nullable=False)

    #mitarbeiter = db.relationship('Mitarbeiter', backref=db.backref('projekt_betreuer', lazy=True))
    #projekt = db.relationship('Projekt', backref=db.backref('projekt_betreuer', lazy=True))


class Wahl(db.Model):
    __tablename__ = 'wahl'
    wahl_id = db.Column(db.Integer, primary_key=True)
    prio = db.Column(db.Integer)
    student_stud_id = db.Column(db.Integer, db.ForeignKey('student.stud_id'), nullable=False)
    projekt_projekt_id = db.Column(db.Integer, db.ForeignKey('projekt.projekt_id'), nullable=False)

    student = db.relationship('Student', backref=db.backref('wahl', lazy=True))
    projekt = db.relationship('Projekt', backref=db.backref('wahl', lazy=True))


class Phase(db.Model):
    __tablename__ = 'phase'
    phase_id = db.Column(db.Integer, primary_key=True)
    semester = db.Column(db.String(20))
    start_p1 = db.Column(db.DateTime)
    ende_p1 = db.Column(db.DateTime)
    start_p2 = db.Column(db.DateTime)
    ende_p2 = db.Column(db.DateTime)
    start_p3 = db.Column(db.DateTime)
    ende_p3 = db.Column(db.DateTime)


class Superuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nds = db.Column(db.String(8))

    def get_all_superusers():
        query = Superuser.query.filter().all()
        all_users = []
        for entry in query:
            all_users.append(entry.nds)
        return all_users
