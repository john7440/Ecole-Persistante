#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""
from business.school import School
from ecole.daos.course_dao import CourseDao


def main() -> None:
    """Programme principal."""
    print("""\
--------------------------
Bienvenue dans notre école
--------------------------""")

    school: School = School()

    # initialisation d'un ensemble de cours, enseignants et élèves composant l'école
    school.init_static()

    # affichage de la liste des cours, leur enseignant et leurs élèves
    school.display_courses_list()

    print('---------------Courses---------------')
    course_dao = CourseDao()
    all_courses = course_dao.read_all()
    for c in all_courses:
        print(f"{c.id} - {c.name} ({c.start_date} → {c.end_date})")


if __name__ == '__main__':
    main()
