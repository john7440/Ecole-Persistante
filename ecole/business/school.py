# -*- coding: utf-8 -*-

"""
Classe School
"""

from dataclasses import dataclass, field
from datetime import date

from ecole.daos.course_dao import CourseDao
from ecole.daos.student_dao import StudentDao
from ecole.daos.teacher_dao import TeacherDao
from ecole.daos.address_dao import AddressDao
from ecole.models.address import Address
from ecole.models.course import Course
from ecole.models.teacher import Teacher
from ecole.models.student import Student


# noinspection SpellCheckingInspection
@dataclass
class School:
    """Couche métier de l'application de gestion d'une école,
    reprenant les cas d'utilisation et les spécifications fonctionnelles :
    - courses : liste des cours existants
    - teachers : liste des enseignants
    - students : liste des élèves"""

    courses: list[Course] = field(default_factory=list, init=False)
    teachers: list[Teacher] = field(default_factory=list, init=False)
    students: list[Student] = field(default_factory=list, init=False)

    def add_course(self, course: Course) -> None:
        """Ajout du cours course à la liste des cours."""
        self.courses.append(course)

    def add_teacher(self, teacher: Teacher) -> None:
        """Ajout de l'enseignant teacher à la liste des enseignants."""
        self.teachers.append(teacher)

    def add_student(self, student: Student) -> None:
        """Ajout de l'élève spécifié à la liste des élèves."""
        self.students.append(student)

    def display_courses_list(self) -> None:
        """Affichage de la liste des cours avec pour chacun d'eux
        - leur enseignant
        - la liste des élèves le suivant"""
        for course in self.courses:
            print(f"cours de {course}")
            for student in course.students_taking_it:
                print(f"- {student}")
            print()

    #============== gestion cours======================
    @staticmethod
    def get_course_by_id(id_course: int):
        course_dao: CourseDao = CourseDao()
        return course_dao.read(id_course)

    @staticmethod
    def create_course(name: str,start_date: date, end_date: date, id_teacher: int) -> str:

        course_dao: CourseDao = CourseDao()
        new_course = Course(
            name=name,
            start_date=start_date,
            end_date=end_date,
            id_teacher=id_teacher
        )

        new_id = course_dao.create(new_course)

        if new_id > 0:
            return (
                f"Cours créé avec succès (id={new_id}): "
                f"{name}, du {start_date} au {end_date}, enseignant id={id_teacher}"
            )
        else:
            return "Échec de la création du cours."


    @staticmethod
    def update_course_by_id(id_course: int, name: str, start_date : date, end_date: date) -> bool:
        course_dao: CourseDao = CourseDao()
        course = course_dao.read(id_course)

        if course is None:
            print(f"Aucun cours trouvée avec id: {id_course}")
            return False

        course.name = name
        course.start_date = start_date
        course.end_date = end_date

        success = course_dao.update(course)

        if success:
            print(f"Cour mis à jour avec succès (id:{id_course})")
        else:
            print(f"Échec de la mise à jour du cours (id:{id_course})")

        return success

    @staticmethod
    def delete_course_by_id(id_course: int) -> bool:
        """
        Supprime un cours en BD via son identifiant
        :param id_course: id du cours à supprimer
        :return: True si la suppression a réussi, False sinon
        """
        course_dao: CourseDao = CourseDao()
        course = course_dao.read(id_course)

        if course is None:
            print(f"Aucun cours trouvée avec id={id_course}")
            return False

        success = course_dao.delete(course)

        if success:
            print(f"Cours supprimée avec succès (id={id_course})")
        else:
            print(f"Échec de la suppression du cours (id={id_course})")

        return success

    @staticmethod
    def get_all_courses() -> str:
        course_dao: CourseDao = CourseDao()
        courses = course_dao.read_all()
        result = ""
        for c in courses:
            result += (
                f"{c.id} - {c.name} ({c.start_date} → {c.end_date})\n"
            )
        return result

    #================Gestion des teachers====================
    @staticmethod
    def create_new_teacher(first_name: str, last_name: str, age: int, hiring_date: date) -> str:
        """
        Crée un nouvel enseignant en BD via le DAO
        :param first_name: prénom du professeur
        :param last_name: nom du professeur
        :param age: âge du professeur
        :param hiring_date: date d'embauche (format 'YYYY-MM-DD')
        :return: message indiquant le succès ou l'échec
        """
        teacher_dao: TeacherDao = TeacherDao()
        new_teacher = Teacher(
            first_name=first_name,
            last_name=last_name,
            age=age,
            hiring_date=hiring_date
        )

        new_id = teacher_dao.create(new_teacher)

        if new_id > 0:
            return f"Professeur créé avec succès (id={new_id}): {first_name} {last_name}, {age} ans, embauché le {hiring_date}"
        else:
            return "Échec de la création du professeur!"

    @staticmethod
    def get_teacher_by_id(id_teacher: int):
        teacher_dao: TeacherDao = TeacherDao()
        return teacher_dao.read(id_teacher)

    @staticmethod
    def update_teacher_by_id(id_teacher: int, first_name: str, last_name: str, age: int, hiring_date: date) -> bool:
        teacher_dao: TeacherDao = TeacherDao()
        teacher = teacher_dao.read(id_teacher)

        if teacher is None:
            print(f"Aucun professeur trouvée avec id={id_teacher}")
            return False

        teacher.first_name = first_name
        teacher.last_name = last_name
        teacher.age = age
        teacher.hiring_date = hiring_date

        success = teacher_dao.update(teacher)

        if success:
            print(f"Professeur mis à jour avec succès (id={id_teacher})")
        else:
            print(f"Échec de la mise à jour du professeur (id={id_teacher})")

        return success

    @staticmethod
    def delete_teacher_by_id(id_teacher: int) -> bool:
        """
        Supprime un teacher en BD via son identifiant
        :param id_teacher: id du teacher à supprimer
        :return: True si la suppression a réussi, False sinon
        """
        teacher_dao: TeacherDao = TeacherDao()
        teacher = teacher_dao.read(id_teacher)

        if teacher is None:
            print(f"Aucun professeur trouvée avec id={id_teacher}")
            return False

        success = teacher_dao.delete(teacher)

        if success:
            print(f"Elève supprimée avec succès (id={id_teacher})")
        else:
            print(f"Échec de la suppression de l'élève (id={id_teacher})")

        return success



    #=================Gestion des Students=================
    @staticmethod
    def create_new_student(first_name: str, last_name: str, age: int) -> str:
        student_dao: StudentDao = StudentDao()
        new_student = Student(
            first_name=first_name,
            last_name=last_name,
            age=age
        )

        new_id = student_dao.create(new_student)

        if new_id > 0:
            return f"Elève créé avec succès (id={new_id}): {first_name} {last_name}, {age} ans!"
        else:
            return "Échec de la création de l'élève!"

    @staticmethod
    def get_student_by_id(id_student: int):
        student_dao: StudentDao = StudentDao()
        return student_dao.read(id_student)

    @staticmethod
    def update_student_by_id(id_student: int, first_name: str, last_name: str, age: int) -> bool:
        student_dao: StudentDao =  StudentDao()
        student = student_dao.read(id_student)

        if student is None:
            print(f"Aucune élève trouvée avec id={id_student}")
            return False

        student.first_name = first_name
        student.last_name = last_name
        student.age = age

        success = student_dao.update(student)

        if success:
            print(f"Elève mise à jour avec succès (id={id_student})")
        else:
            print(f"Échec de la mise à jour de l'élève (id={id_student})")

        return success

    @staticmethod
    def delete_student_by_id(id_student: int) -> bool:
        """
        Supprime un élève en BD via son identifiant
        :param id_student: identifiant de l'élève à supprimer
        :return: True si la suppression a réussi, False sinon
        """
        student_dao: StudentDao = StudentDao()
        student = student_dao.read(id_student)

        if student is None:
            print(f"Aucun élève trouvée avec id={id_student}")
            return False

        success = student_dao.delete(student)

        if success:
            print(f"Elève supprimée avec succès (id={id_student})")
        else:
            print(f"Échec de la suppression de l'élève (id={id_student})")

        return success

    #==============gestion des adresses============
    @staticmethod
    def get_address_by_id(id_address: int):
        address_dao: AddressDao = AddressDao()
        return address_dao.read(id_address)

    @staticmethod
    def get_all_addresses() -> str:
        address_dao: AddressDao = AddressDao()
        adresses = address_dao.read_all()
        result = ""
        for a in adresses:
            result += (
                f"{a.street}, {a.postal_code}: {a.city}\n"
            )
        return result

    @staticmethod
    def create_new_address(street: str, city: str, postal_code: int) -> str:
        address_dao: AddressDao = AddressDao()
        new_address = Address(street=street, city=city, postal_code=postal_code)

        new_id = address_dao.create(new_address)
        if new_id > 0:
            return f"Adresse créée avec succès (id={new_id}): {street}, {postal_code} {city})"
        else:
            return "Échec de la création de l'adresse! "

    @staticmethod
    def update_address_by_id(id_address: int, street: str, city: str, postal_code: int) -> bool:
        """
        Met à jour une adresse en BD via son id
        :param id_address: identifiant de l'adresse à mettre à jour
        :param street: nouvelle rue
        :param city: nouvelle ville
        :param postal_code: nouveau code postal
        :return: True si la mise à jour a réussi sinon False
        """
        address_dao: AddressDao = AddressDao()
        address = address_dao.read(id_address)

        if address is None:
            print(f"Aucune adresse trouvée avec id={id_address}")
            return False

        address.street = street
        address.city = city
        address.postal_code = postal_code

        success = address_dao.update(address)

        if success:
            print(f"Adresse mise à jour avec succès (id={id_address})")
        else:
            print(f"Échec de la mise à jour de l'adresse (id={id_address})")

        return success


    @staticmethod
    def delete_address_by_id(id_address: int) -> bool:
        """
        Supprime une adresse en BD via son identifiant
        :param id_address: identifiant de l'adresse à supprimer
        :return: True si la suppression a réussi, False sinon
        """
        address_dao: AddressDao = AddressDao()
        address = address_dao.read(id_address)

        if address is None:
            print(f"Aucune adresse trouvée avec id={id_address}")
            return False

        success = address_dao.delete(address)

        if success:
            print(f"Adresse supprimée avec succès (id={id_address})")
        else:
            print(f"Échec de la suppression de l'adresse (id={id_address})")

        return success

    @staticmethod
    def get_all_teachers() -> str:
        teacher_dao: TeacherDao = TeacherDao()
        teachers = teacher_dao.read_all()
        result = ""
        for t in teachers:
            result += (
                f"Prénom: {t.first_name}\nNom: {t.last_name}\nAge: {t.age}\nDate d'embauche: {t.hiring_date}\n\n"
            )
        return result

    @staticmethod
    def get_all_students() -> str:
        student_dao: StudentDao = StudentDao()
        students = student_dao.read_all()
        result = ""
        for s in students:
            result += (
                f"Prénom: {s.first_name}\nNom: {s.last_name}\nAge: {s.age}\n\n"
            )
        return result

    @staticmethod
    def print_all_database():
        school = School()
        print('---------------Courses---------------\n')
        print(school.get_all_courses())
        print('---------------Adresses---------------\n')
        print(school.get_all_addresses())
        print('---------------Teachers---------------\n')
        print(school.get_all_teachers())
        print('---------------Students---------------\n')
        print(school.get_all_students())


    def init_static(self) -> None:
        """Initialisation d'un jeu de test pour l'école."""
        
        # création des étudiants et rattachement à leur adresse
        paul: Student    = Student('Paul', 'Dubois', 12)
        valerie: Student = Student('Valérie', 'Dumont', 13)
        louis: Student   = Student('Louis', 'Berthot', 11)

        paul.address    = Address('12 rue des Pinsons', 'Castanet', 31320)
        valerie.address = Address('43 avenue Jean Zay', 'Toulouse', 31200)
        louis.address   = Address('7 impasse des Coteaux', 'Cornebarrieu', 31150)

        # ajout de ceux-ci à l'école
        for student in [paul, valerie, louis]:
            self.add_student(student)

        # création des cours
        francais: Course = Course("Français", date(2024, 1, 29),
                                              date(2024, 2, 16))
        histoire: Course = Course("Histoire", date(2024, 2, 5),
                                              date(2024, 2, 16))
        geographie: Course = Course("Géographie", date(2024, 2, 5),
                                                  date(2024, 2, 16))
        mathematiques: Course = Course("Mathématiques", date(2024, 2, 12),
                                                        date(2024, 3, 8))
        physique: Course = Course("Physique", date(2024, 2, 19),
                                              date(2024, 3, 8))
        chimie: Course = Course("Chimie", date(2024, 2, 26),
                                          date(2024, 3, 15))
        anglais: Course = Course("Anglais", date(2024, 2, 12),
                                            date(2024, 2, 24))
        sport: Course = Course("Sport", date(2024, 3, 4),
                                        date(2024, 3, 15))

        # ajout de ceux-ci à l'école
        for course in [francais, histoire, geographie, mathematiques,
                       physique, chimie, anglais, sport]:
            self.add_course(course)

        # création des enseignants
        victor  = Teacher('Victor', 'Hugo', 23, date(2023, 9, 4))
        jules   = Teacher('Jules', 'Michelet', 32, date(2023, 9, 4))
        sophie  = Teacher('Sophie', 'Germain', 25, date(2023, 9, 4))
        marie   = Teacher('Marie', 'Curie', 31, date(2023, 9, 4))
        william = Teacher('William', 'Shakespeare', 34, date(2023, 9, 4))
        michel  = Teacher('Michel', 'Platini', 42, date(2023, 9, 4))

        # ajout de ceux-ci à l'école
        for teacher in [victor, jules, sophie, marie, william, michel]:
            self.add_teacher(teacher)

        # association des élèves aux cours qu'ils suivent
        for course in [geographie, physique, anglais]:
            paul.add_course(course)

        for course in [francais, histoire, chimie]:
            valerie.add_course(course)

        for course in [mathematiques, physique, geographie, sport]:
            louis.add_course(course)

        # association des enseignants aux cours qu'ils enseignent
        victor.add_course(francais)

        jules.add_course(histoire)
        jules.add_course(geographie)

        sophie.add_course(mathematiques)

        marie.add_course(physique)
        marie.add_course(chimie)

        william.add_course(anglais)

        michel.add_course(sport)
