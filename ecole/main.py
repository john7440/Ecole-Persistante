#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""

from ecole.daos.address_dao import AddressDao
from ecole.daos.course_dao import CourseDao
from ecole.daos.student_dao import StudentDao
from ecole.daos.teacher_dao import TeacherDao


def main() -> None:
    """Programme principal."""
    print("""\
--------------------------
Bienvenue dans notre école
--------------------------""")

    print('---------------Courses---------------')
    course_dao = CourseDao()
    all_courses = course_dao.read_all()
    for c in all_courses:
        print(f"{c.id} - {c.name} ({c.start_date} → {c.end_date})")

    print('---------------Adresses---------------')
    address_dao = AddressDao()
    adresses = address_dao.read_all()
    for a in adresses:
        print(f"{a.street}, {a.postal_code}: {a.city}")

    print('---------------Teachers---------------')
    teacher_dao = TeacherDao()
    teachers = teacher_dao.read_all()
    for t in teachers:
        print(f"Prénom: {t.first_name}\nNom: {t.last_name}\nAge: {t.age}\nDate d\'embauche: {t.hiring_date}\n")

    print('---------------Students---------------')
    student_dao = StudentDao()
    students = student_dao.read_all()
    for s in students:
        print(f"Prénom: {s.first_name}\nNom: {s.last_name}\nAge: {s.age}\n")


if __name__ == '__main__':
    main()
