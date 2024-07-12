from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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

    # return a list of all study programs
    @staticmethod
    def get_all_studiengaenge():
        return Studiengang.query.all()

class Fach(db.Model):
    __tablename__ = 'fach'
    fach_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bezeichnung = db.Column(db.String(50))

    # return a list of all subjects
    @staticmethod
    def get_all_faecher():
        return Fach.query.all()

class Art(db.Model):
    __tablename__ = 'art'
    art_id = db.Column(db.Integer, primary key=True, autoincrement=True)
    art_typ = db.Column(db.String(30))

    students = db.relationship('Student', secondary='student_art', back_populates='arten')

    # return a list of all distinct types of seminar work
    @staticmethod
    def get_all_arten():
        return Art.query.distinct(Art.art_typ).all()

    # return the color assigned to an art type (used in employee profile)
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

    # return the badge (color tag) with the initial letter and corresponding color of the art type (used in topic overview, admin profile)
    def get_badge(self):
        if self.art_typ == 'Bachelorarbeit':
            return 'w3-blue', 'B'
        elif self.art_typ == 'Masterarbeit':
            return 'w3-green', 'M'
        elif self.art_typ == 'Projektseminar':
            return 'w3-yellow', 'P'
        elif self.art_typ == 'Praxisseminar':
            return 'w3-red', 'P'
        elif self.art_typ == 'Theoretisches Seminar':
            return 'w3-purple', 'T'
        else:
            return 'w3-grey', ''

class Lehrstuhl(db.Model):
    __tablename__ = 'lehrstuhl'
    lehrstuhl_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    professor = db.Column(db.String(100))
    homepage = db.Column(db.String(100))

    # return a list of all chairs
    @staticmethod
    def get_all_lehrstuehle():
        return Lehrstuhl.query.all()

    # return all projects of a specific chair (self)
    def get_lehrstuhl_projekte(self):
        return Projekt.query.filter_by(lehrstuhl_lehrstuhl_id=self.lehrstuhl_id).all()

    # create a new chair
    @staticmethod
    def create_lehrstuhl(name, homepage, professor):
        lehrstuhl = Lehrstuhl(
            name=name,
            homepage=homepage,
            professor=professor
        )
        db.session.add(lehrstuhl)
        db.session.commit()
        return lehrstuhl

    # edit an existing chair
    def edit_lehrstuhl(self, name, homepage, professor):
        edited = (
            db.update(Lehrstuhl).
            where(Lehrstuhl.lehrstuhl_id == self.lehrstuhl_id).
            values(
                name=name,
                homepage=homepage,
                professor=professor
            )
        )
        db.session.execute(edited)
        db.session.commit()

    # delete an existing chair
    def delete_lehrstuhl(self):
        db.session.delete(self)
        db.session.commit()
        return self

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

    # create a new student
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

    # edit an existing student
    @staticmethod
    def edit_student(self, vorname, nachname, nds, email, matrikelnummer, studiengang_id):
        edited = (
            db.update(Student).
            where(Student.stud_id == self.stud_id).
            values(
                vorname=vorname,
                nachname=nachname,
                nds=nds,
                email=email,
                matrikelnummer=matrikelnummer,
                studiengang_studiengang_id=studiengang_id
            )
        )
        db.session.execute(edited)
        db.session.commit()

    # delete an existing student
    def delete_student(self):
        db.session.delete(self)
        db.session.commit()
        return self

    # delete all student records
    @staticmethod
    def delete_all_students():
        students = Student.query.all()
        for student in students:
            student.delete_student()
        db.session.commit()

    # add specific types (arten_ids) to the selected types of an existing student
    def add_arten(self, arten_ids):
        for art_id in arten_ids:
            art = Art.query.get(int(art_id))
            if art:
                self.arten.append(art)
        db.session.commit()

    # remove a specific type (art_id) from the selected types of an existing student
    def remove_art(self, art_id):
        art = Art.query.get(art_id)
        if art in self.get_selected_arten():
            self.arten.remove(art)
            Wahl.query.filter_by(student_stud_id=self.stud_id, art_art_id=art_id).delete()
            db.session.commit()

    # return a list of selected types for a student
    def get_selected_arten(self):
        return self.arten

    # return a list of all students
    @staticmethod
    def get_all_Students():
        return Student.query.all()

    # return the student based on the nds
    def get_student(nds=""):
        student = None
        if nds != "":
            student = Student.query.filter_by(nds=nds).first()
        return student

class StudentArt(db.Model):
    __tablename__ = 'student_art'
    stud_art_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    art_art_id = db.Column(db.Integer, db.ForeignKey('art.art_id'))
    student_stud_id = db.Column(db.Integer, db.ForeignKey('student.stud_id', ondelete='CASCADE'))


class Mitarbeiter(db.Model):
    __tablename__ = 'mitarbeiter'
    ma_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vorname = db.Column(db.String(20))
    nachname = db.Column(db.String(30))
    nds = db.Column(db.String(10))
    email = db.Column(db.String(50))
    lehrstuhl_lehrstuhl_id = db.Column(db.Integer, db.ForeignKey('lehrstuhl.lehrstuhl_id'), nullable=False)

    lehrstuhl = db.relationship('Lehrstuhl', backref='lehrstuhl_mitarbeiter', lazy=True)

    betreute_projekte = db.relationship('Projekt', secondary='projekt_mitarbeiter', back_populates='betreuer')

    # create a new employee
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

    # edit an existing employee
    def edit_mitarbeiter(self, vorname, nachname, email, nds, lehrstuhl_id):
        edited = (
            db.update(Mitarbeiter).
            where(Mitarbeiter.ma_id == self.ma_id).
            values(
                vorname=vorname,
                nachname=nachname,
                email=email,
                nds=nds,
                lehrstuhl_lehrstuhl_id=lehrstuhl_id
            )
        )
        db.session.execute(edited)
        db.session.commit()

    # delete an existing employee
    def delete_mitarbeiter(self):
        db.session.delete(self)
        db.session.commit()
        return self

    # return a list of all employees
    @staticmethod
    def get_all_Mitarbeiter():
        return Mitarbeiter.query.all()

    # return the employee based on the NDS identifier
    @staticmethod
    def get_mitarbeiter(nds=""):
        mitarbeiter = None
        if nds != "":
            mitarbeiter = Mitarbeiter.query.filter_by(nds=nds).first()
        return mitarbeiter

    # return a list of all unique NDS identifiers
    @staticmethod
    def get_all_nds():
        query = Mitarbeiter.query.filter(Mitarbeiter.nds != "0").all()
        all_nds = []
        for entry in query:
            all_nds.append(entry.nds)
        return all_nds

    # group employees by their chair (returns dictionary)
    @staticmethod
    def group_by_lehrstuhl(mitarbeiter):
        lehrstuhl_dict = {}
        for ma in mitarbeiter:
            lehrstuhl = ma.lehrstuhl
            if lehrstuhl not in lehrstuhl_dict:
                lehrstuhl_dict[lehrstuhl] = []
            lehrstuhl_dict[lehrstuhl].append(ma)
        return lehrstuhl_dict


class Projekt(db.Model):
    __tablename__ = 'projekt'
    projekt_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titel = db.Column(db.String(200))
    beschreibung = db.Column(db.String(2500))
    max_anzahl = db.Column(db.Integer)
    neu = db.Column(db.Boolean)
    studiengang_studiengang_id = db.Column(db.Integer, db.ForeignKey('studiengang.studiengang_id'), nullable=False)
    fach_fach_id = db.Column(db.Integer, db.ForeignKey('fach.fach_id'), nullable=False)
    art_art_id = db.Column(db.Integer, db.ForeignKey('art.art_id'), nullable=False)
    lehrstuhl_lehrstuhl_id = db.Column(db.Integer, db.ForeignKey('lehrstuhl.lehrstuhl_id'), nullable=False)

    studiengang = db.relationship('Studiengang', backref=db.backref('projekt', lazy=True))
    fach = db.relationship('Fach', backref=db.backref('projekt', lazy=True))
    art = db.relationship('Art', backref=db.backref('projekte', lazy=True))
    lehrstuhl = db.relationship('Lehrstuhl', backref=db.backref('projekt', lazy=True))

    betreuer = db.relationship('Mitarbeiter', secondary='projekt_mitarbeiter', back_populates='betreute_projekte')

    # create a new project
    @staticmethod
    def create_projekt(titel, beschreibung, max_anzahl, studiengang_id, fach_id, art_id, lehrstuhl_id, betreuer_ids):
        projekt = Projekt(
            titel=titel,
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

    # add supervisors to a project (entries in the intermediate table ProjektMitarbeiter)
    def add_projekt_betreuer(self, mitarbeiter_ids):
        for ma_id in mitarbeiter_ids:
            mitarbeiter = Mitarbeiter.query.get(int(ma_id))
            if mitarbeiter:
                self.betreuer.append(mitarbeiter)

    # edit an existing project
    def edit_projekt(self, titel, beschreibung, max_anzahl, studiengang_id, lehrstuhl_id, art_id, fach_id, betreuer_ids):
        edited = (
            db.update(Projekt).
            where(Projekt.projekt_id == self.projekt_id).
            values(
                titel=titel,
                beschreibung=beschreibung,
                max_anzahl=max_anzahl,
                studiengang_studiengang_id=studiengang_id,
                lehrstuhl_lehrstuhl_id=lehrstuhl_id,
                art_art_id=art_id,
                fach_fach_id=fach_id
            )
        )
        db.session.execute(edited)
        self.betreuer.clear()
        self.add_projekt_betreuer(betreuer_ids)
        db.session.commit()

    # delete an existing project
    def delete_projekt(self):
        db.session.delete(self)
        db.session.commit()
        return self

    # return projects filtered by a keyword, their type, or their chair
    @staticmethod
    def get_projects_by(search_query=None, art_filter=None, lehrstuhl_filter=None):
        projekte = Projekt.query
        if search_query:
            projekte = Projekt.apply_keyword_search(projekte, search_query)
        if art_filter:
            projekte = projekte.join(Projekt.art).filter(Art.art_typ == art_filter)
        if lehrstuhl_filter:
            projekte = projekte.join(Projekt.lehrstuhl).filter(Lehrstuhl.lehrstuhl_id == lehrstuhl_filter)
        return projekte.all()

    # perform a keyword search for a list of projects based on title, subject, etc.
    @staticmethod
    def apply_keyword_search(projekte, search_query):
        if search_query:
            search_filter = f"%{search_query}%"
            projekte = projekte.filter(
                (Projekt.titel.ilike(search_filter)) |
                # (Projekt.beschreibung.ilike(search_filter)) |
                (Fach.bezeichnung.ilike(search_filter)) |
                (Studiengang.bezeichnung.ilike(search_filter)) |
                (Studiengang.abschluss.ilike(search_filter)) |
                (Projekt.betreuer.any(Mitarbeiter.vorname.ilike(search_query))) |
                (Projekt.betreuer.any(Mitarbeiter.nachname.ilike(search_query)))
            )
        return projekte

    # sort projects alphabetically by their name
    @staticmethod
    def order_ascending_by_name(projekte):
        return sorted(projekte, key=lambda projekt: projekt.titel)

    # group projects by their type
    @staticmethod
    def group_by_art():
        projekte = Projekt.query.join(Art, Projekt.art_art_id == Art.art_id).order_by(Art.art_typ, Projekt.titel).all()
        art_dict = {}
        for projekt in projekte:
            art = projekt.art
            if art not in art_dict:
                art_dict[art] = []
            art_dict[art].append(projekt)
        return art_dict

    # group projects by their chair
    @staticmethod
    def group_by_lehrstuhl(projekte):
        lehrstuhl_dict = {}
        for projekt in projekte:
            lehrstuhl = projekt.lehrstuhl
            if lehrstuhl not in lehrstuhl_dict:
                lehrstuhl_dict[lehrstuhl] = []
            lehrstuhl_dict[lehrstuhl].append(projekt)

        # sort projects within each chair by art_id
        for lehrstuhl in lehrstuhl_dict:
            lehrstuhl_dict[lehrstuhl] = sorted(lehrstuhl_dict[lehrstuhl], key=lambda projekt: projekt.art_art_id)

        # sort the dictionary by the chair's lehrstuhl_id
        sorted_lehrstuhl_dict = {k: lehrstuhl_dict[k] for k in
                                 sorted(lehrstuhl_dict, key=lambda lehrstuhl: lehrstuhl.lehrstuhl_id)}

        return sorted_lehrstuhl_dict

    # mark all projects as old
    @staticmethod
    def mark_all_as_old():
        projects = Projekt.query.all()
        for project in projects:
            project.neu = False
        db.session.commit()

class ProjektMitarbeiter(db.Model):
    __tablename__ = 'projekt_mitarbeiter'
    pb_id = db.Column(db.Integer, primary key=True)
    mitarbeiter_ma_id = db.Column(db.Integer, db.ForeignKey('mitarbeiter.ma_id', ondelete='CASCADE'), nullable=False)
    projekt_projekt_id = db.Column(db.Integer, db.ForeignKey('projekt.projekt_id', ondelete='CASCADE'), nullable=False)

class Wahl(db.Model):
    __tablename__ = 'wahl'
    wahl_id = db.Column(db.Integer, primary key=True, autoincrement=True)
    prio = db.Column(db.Integer)
    student_stud_id = db.Column(db.Integer, db.ForeignKey('student.stud_id', ondelete='CASCADE'), nullable=False)
    projekt_projekt_id = db.Column(db.Integer, db.ForeignKey('projekt.projekt_id', ondelete='RESTRICT'), nullable=False)
    art_art_id = db.Column(db.Integer, db.ForeignKey('art.art_id'), nullable=False)

    student = db.relationship('Student', backref=db.backref('wahl', lazy=True, cascade='all, delete-orphan'))
    projekt = db.relationship('Projekt', backref=db.backref('wahl', lazy=True, cascade='none'))
    art = db.relationship('Art', backref=db.backref('wahl'), lazy=True)

    # save the priorities of a student for a specific type
    @staticmethod
    def save_priorities(student_id, art_id, priorities):
        Wahl.delete_priorities(student_id, art_id)
        for prio, projekt_id in priorities.items():
            wahl = Wahl(
                student_stud_id=student_id,
                projekt_projekt_id=projekt_id,
                art_art_id=art_id,
                prio=prio
            )
            db.session.add(wahl)
        db.session.commit()

    # return the priorities of a student for a specific type
    @staticmethod
    def get_priorities_for_art(student_id, art_id):
        wahl = Wahl.query.filter_by(student_stud_id=student_id, art_art_id=art_id).all()
        if not wahl:
            return None
        priorities = {
            1: next((Projekt.query.get(w.projekt_projekt_id) for w in wahl if w.prio == 1), None),
            2: next((Projekt.query.get(w.projekt_projekt_id) for w in wahl if w.prio == 2), None),
            3: next((Projekt.query.get(w.projekt_projekt_id) for w in wahl if w.prio == 3), None)
        }
        return priorities

    # delete the priorities of a student for a specific type
    @staticmethod
    def delete_priorities(student_id, art_id):
        Wahl.query.filter_by(student_stud_id=student_id, art_art_id=art_id).delete()
        db.session.commit()


    # return a dictionary with the selected types as keys and their associated priorities
    @staticmethod
    def get_all_priorities(student_id):
        wahl = Wahl.query.filter_by(student_stud_id=student_id).all()
        if not wahl:
            # empty if no prioritization for any art
            return {}
        all_priorities = {}
        for w in wahl:
            if w.art_art_id not in all_priorities:
                all_priorities[w.art_art_id] = {}
            all_priorities[w.art_art_id][w.prio] = Projekt.query.get(w.projekt_projekt_id)
        for art_id in all_priorities:
            all_priorities[art_id] = dict(sorted(all_priorities[art_id].items()))
        return all_priorities


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
    start_vorstellung = db.Column(db.DateTime)
    ende_vorstellung = db.Column(db.DateTime)

    # create phase data for a specific semester
    @staticmethod
    def create_phasen(semester, jahr, start_p1, ende_p1, start_p2, ende_p2, start_p3, ende_p3, start_vorstellung, ende_vorstellung):
        if semester == 'Wintersemester':
            semester_formatted = f"{semester} {jahr}/{int(jahr) + 1}"
        else:
            semester_formatted = f"{semester} {jahr}"

        new = Phase(
            semester=semester_formatted,
            start_p1=start_p1,
            ende_p1=ende_p1,
            start_p2=start_p2,
            ende_p2=ende_p2,
            start_p3=start_p3,
            ende_p3=ende_p3,
            start_vorstellung=start_vorstellung,
            ende_vorstellung=ende_vorstellung
        )
        db.session.add(new)
        db.session.commit()

    # edit existing phase data
    def edit_phasen(self, start_p1, ende_p1, start_p2, ende_p2, start_p3, ende_p3, start_vorstellung, ende_vorstellung):
        edited = (
            db.update(Phase).
            where(Phase.phase_id == self.phase_id).
            values(
                start_p1=start_p1,
                ende_p1=ende_p1,
                start_p2=start_p2,
                ende_p2=ende_p2,
                start_p3=start_p3,
                ende_p3=ende_p3,
                start_vorstellung=start_vorstellung,
                ende_vorstellung=ende_vorstellung
            )
        )
        db.session.execute(edited)
        db.session.commit()

    # delete a phase
    def delete_phasen(self):
        db.session.delete(self)
        db.session.commit()

    # return the current phase
    @staticmethod
    def get_current():
        return Phase.query.order_by(Phase.phase_id.desc()).first()

    # check if phase 1 of the allocation process is active
    def p1_active(self):
        current_time = datetime.now()
        return self.start_p1 <= current_time <= self.ende_p1

    # check if phase 2 of the allocation process is active
    def p2_active(self):
        current_time = datetime.now()
        return self.start_p2 <= current_time <= self.ende_p2

    # check if phase 3 of the allocation process is active
    def p3_active(self):
        current_time = datetime.now()
        return self.start_p3 <= current_time <= self.ende_p3

class User(UserMixin):
    def __init__(self, nds, vorname, nachname, mail):
        self.nds = nds
        self.vorname = vorname
        self.nachname = nachname
        self.mail = mail

    def get_id(self):
        return self.nds

    # check if user is a student
    @property
    def is_student(self):
        return Student.query.filter_by(nds=self.nds).first() is not None

    # check if user is an employee
    @property
    def is_mitarbeiter(self):
        return Mitarbeiter.query.filter_by(nds=self.nds).first() is not None

class Superuser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nds = db.Column(db.String(8))

    # check if user has an entry in the superuser table based on his nds
    @staticmethod
    def is_admin(nds):
        return Superuser.query.filter_by(nds=nds).first() is not None
