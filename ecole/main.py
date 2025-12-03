#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""
from ecole.business.school import School
from ecole.daos.address_dao import AddressDao



def main() -> None:
    """Programme principal."""
    print("""\
-----------------------------------------
       Bienvenue dans notre école
-----------------------------------------""")

    school = School()

    print('---------------Courses---------------\n')
    print(school.get_all_courses())

    print('---------------Adresses---------------\n')
    print(school.get_all_addresses())

    print('---------------Teachers---------------\n')
    print(school.get_all_teachers())

    print('---------------Students---------------\n')
    print(school.get_all_students())


if __name__ == '__main__':
    main()
