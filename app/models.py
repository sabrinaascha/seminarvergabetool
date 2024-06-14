from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta

db = SQLAlchemy()


class Gruppe(db.Model):
    __tablename__ = 'gruppe'
    gruppe_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    status = db.Column(db.Boolean)


class Studiengang(db.Model):
    __tablename__ = 'studiengang'
    studiengang_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bezeichnung = db.Column(db.String(50))
    abschluss = db.Column(db.String(10))

    @staticmethod
    def get_all_studiengaenge():
        return Studiengang.query.all()


class Fach(db.Model):
    __tablename__ = 'fach'
    fach_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bezeichnung = db.Column(db.String(50))

    @staticmethod
    def get_all_faecher():
        return Fach.query.all()

class Art(db.Model):
    __tablename__ = 'art'
    art_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    art_typ = db.Column(db.String(30))

    students = db.relationship('Student', secondary='student_art', back_populates='arten')
    projekte = db.relationship('Projekt', backref=db.backref('arten', lazy=True))

    @staticmethod
    def get_all_arten():
        return Art.query.distinct(Art.art_typ).all()

    def get_color(self):
        if self.art_typ == 'Bachelorarbeit':
            return 'w3-pale-blue'
        elif self.art_typ == 'Masterarbeit':
            return 'w3-pale-green'
        elif self.art_typ == 'Projektseminar':
            return 'w3-pale-yellow'
        elif self.art_typ == 'Praxisseminar':
            return 'w3-pale-red'
        elif self.art_typ == 'Theoretisches Seminar':
            return 'w3-pale-purple'
        return 'w3-light-grey'

    def get_circle_tag(self):
        tags = {
            'Bachelorarbeit': ('w3-blue', 'B'),
            'Masterarbeit': ('w3-green', 'M'),
            'Projektseminar': ('w3-yellow', 'P'),
            'Praxisseminar': ('w3-red', 'P'),
            'Theoretisches Seminar': ('w3-purple', 'T'),
        }
        return tags.get(self.art_typ, ('', ''))


class Lehrstuhl(db.Model):
    __tablename__ = 'lehrstuhl'
    lehrstuhl_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40))
    homepage = db.Column(db.String(50))

    lehrstuhl_mitarbeiter = db.relationship('Mitarbeiter', backref='lehrstuhl', lazy=True)

    @staticmethod
    def get_all_lehrstuehle():
        return Lehrstuhl.query.all()


    def get_lehrstuhl_projekte(self):
        return Projekt.query.filter_by(lehrstuhl_lehrstuhl_id=self.lehrstuhl_id).all()


class Student(db.Model):
    __tablename__ = 'student'
    stud_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
        student = Student(
            vorname=vorname,
            nachname=nachname,
            nds=nds,
            email=email,
            matrikelnummer=matrikelnummer,
            studiengang_studiengang_id=studiengang_id
        )
        db.session.add(student)
        db.session.commit()
        return student

    def add_arten(self, arten_ids):
        for art_id in arten_ids:
            art = Art.query.get(int(art_id))
            if art:
                self.arten.append(art)
        db.session.commit()

    def get_selected_arten(self):
        return self.arten

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
    stud_art_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    art_art_id = db.Column(db.Integer, db.ForeignKey('art.art_id'))
    student_stud_id = db.Column(db.Integer, db.ForeignKey('student.stud_id'))

    #art = db.relationship('Art', backref=db.backref('student_art', lazy=True))
    #student = db.relationship('Student', backref=db.backref('student_art', lazy=True))





class Mitarbeiter(db.Model):
    __tablename__ = 'mitarbeiter'
    ma_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vorname = db.Column(db.String(20))
    nachname = db.Column(db.String(30))
    nds = db.Column(db.String(10))
    email = db.Column(db.String(50))
    lehrstuhl_lehrstuhl_id = db.Column(db.Integer, db.ForeignKey('lehrstuhl.lehrstuhl_id'), nullable=False)

    betreute_projekte = db.relationship('Projekt', secondary='projekt_mitarbeiter', back_populates='betreuer')

    @staticmethod
    def is_mitarbeiter(nds=""):
        return Mitarbeiter.query.filter_by(nds=nds).first() is not None

    @staticmethod
    def create_mitarbeiter(vorname, nachname, nds, email, lehrstuhl_id):
        mitarbeiter = Mitarbeiter(
            vorname=vorname,
            nachname=nachname,
            nds=nds,
            email=email,
            lehrstuhl_lehrstuhl_id=lehrstuhl_id
        )
        db.session.add(mitarbeiter)
        db.session.commit()
        return mitarbeiter

    @staticmethod
    def get_all_Mitarbeiter():
        return Mitarbeiter.query.all()


    @staticmethod
    def get_mitarbeiter(nds=""):
        if nds != "":
            mitarbeiter = Mitarbeiter.query.filter_by(nds=nds).first()
        return mitarbeiter

    @staticmethod
    def get_all_nds():
        query = Mitarbeiter.query.filter(Mitarbeiter.nds != "0").all()
        all_nds = []
        for entry in query:
            all_nds.append(entry.nds)
        return all_nds


class Projekt(db.Model):
    __tablename__ = 'projekt'
    projekt_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

    @staticmethod
    def create_projekt(titel, beschreibung, max_anzahl, studiengang_id, fach_id, art_id, lehrstuhl_id, betreuer_ids):
        projekt = Projekt(
            titel = titel,
            beschreibung=beschreibung,
            max_anzahl=max_anzahl,
            neu=True,
            studiengang_studiengang_id=studiengang_id,
            fach_fach_id=fach_id,
            art_art_id=art_id,
            lehrstuhl_lehrstuhl_id=lehrstuhl_id
        )
        projekt.add_projekt_betreuer(betreuer_ids)
        db.session.add(projekt)
        db.session.commit()
        return projekt

    def add_projekt_betreuer(self, mitarbeiter_ids):
        for ma_id in mitarbeiter_ids:
            mitarbeiter = Mitarbeiter.query.get(int(ma_id))
            if mitarbeiter:
                self.betreuer.append(mitarbeiter)


    def edit_projekt(self, titel, beschreibung, max_anzahl, studiengang_id, art_id, betreuer_ids):
        edited = (
            db.update(Projekt).
            where(Projekt.projekt_id == self.projekt_id).
            values(
                titel=titel,
                beschreibung=beschreibung,
                max_anzahl=max_anzahl,
                studiengang_studiengang_id=studiengang_id,
                art_art_id=art_id
            )
        )
        db.session.execute(edited)

        self.betreuer.clear()
        self.add_projekt_betreuer(betreuer_ids)
        db.session.commit()

    def delete_projekt(self):
        db.session.delete(self)
        db.session.commit()
        return self



    @staticmethod
    def get_projects_by(search_query=None, art_filter=None):
        projekte = Projekt.query
        if search_query:
            projekte = Projekt.apply_keyword_search(projekte, search_query)
        if art_filter:
            projekte = projekte.join(Projekt.art).filter(Art.art_typ == art_filter)
        return projekte.all()

    @staticmethod
    def group_by_lehrstuhl(projekte):
        lehrstuhl_dict = {}
        for projekt in projekte:
            lehrstuhl = projekt.lehrstuhl
            if lehrstuhl not in lehrstuhl_dict:
                lehrstuhl_dict[lehrstuhl] = []
            lehrstuhl_dict[lehrstuhl].append(projekt)
        return lehrstuhl_dict

    @staticmethod
    def apply_keyword_search(projekte, search_query):
        if search_query:
            search_filter = f"%{search_query}%"
            projekte = projekte.filter(
                (Projekt.titel.ilike(search_filter)) |
                #(Projekt.beschreibung.ilike(search_filter)) |
                (Fach.bezeichnung.ilike(search_filter)) |
                (Art.art_typ.ilike(search_filter)) |
                (Projekt.betreuer.any(Mitarbeiter.vorname.ilike(search_query))) |
                (Projekt.betreuer.any(Mitarbeiter.nachname.ilike(search_query)))
            )
        return projekte


class ProjektMitarbeiter(db.Model):
    __tablename__ = 'projekt_mitarbeiter'
    pb_id = db.Column(db.Integer, primary_key=True)
    mitarbeiter_ma_id = db.Column(db.Integer, db.ForeignKey('mitarbeiter.ma_id'), nullable=False)
    projekt_projekt_id = db.Column(db.Integer, db.ForeignKey('projekt.projekt_id'), nullable=False)

    #mitarbeiter = db.relationship('Mitarbeiter', backref=db.backref('projekt_betreuer', lazy=True))
    #projekt = db.relationship('Projekt', backref=db.backref('projekt_betreuer', lazy=True))


class Wahl(db.Model):
    __tablename__ = 'wahl'
    wahl_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prio = db.Column(db.Integer)
    student_stud_id = db.Column(db.Integer, db.ForeignKey('student.stud_id'), nullable=False)
    projekt_projekt_id = db.Column(db.Integer, db.ForeignKey('projekt.projekt_id'), nullable=False)

    student = db.relationship('Student', backref=db.backref('wahl', lazy=True))
    projekt = db.relationship('Projekt', backref=db.backref('wahl', lazy=True))

    @staticmethod
    def save_priorities(student_id, priorities):
        for project_id, priority in priorities:
            wahl_entry = Wahl(
                prio=priority,
                student_stud_id=student_id,
                projekt_projekt_id=project_id
            )
            db.session.add(wahl_entry)
        db.session.commit()


class Phase(db.Model):
    __tablename__ = 'phase'
    phase_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    semester = db.Column(db.String(20))
    start_p1 = db.Column(db.DateTime)
    ende_p1 = db.Column(db.DateTime)
    start_p2 = db.Column(db.DateTime)
    ende_p2 = db.Column(db.DateTime)
    start_p3 = db.Column(db.DateTime)
    ende_p3 = db.Column(db.DateTime)

class User(UserMixin):
    def __init__(self, nds, vorname, nachname, mail):
        self.nds = nds
        self.vorname = vorname
        self.nachname = nachname
        self.mail = mail

    def get_id(self):
        return self.nds

    @property
    def is_student(self):
        return Student.query.filter_by(nds=self.nds).first() is not None

    @property
    def is_mitarbeiter(self):
        return Mitarbeiter.query.filter_by(nds=self.nds).first() is not None


class Superuser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nds = db.Column(db.String(8))

    @staticmethod
    def get_all_superusers():
        query = Superuser.query.all()
        all_users = []
        for entry in query:
            all_users.append(entry.nds)
        return all_users
