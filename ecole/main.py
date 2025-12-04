#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""
import datetime
from ecole.business.school import School


def main() -> None:
    """Programme principal."""
    print("""\
-----------------------------------------
       Bienvenue dans notre école
-----------------------------------------""")

    school = School()

    #ajout d'adresse
    #school.create_new_address(street="3 Rue de la pierre en Bois", city="Paris", postal_code=75000)
    #school.create_new_address(street='1 Avenue du Pain-au-Chocolat', city='Cookieland', postal_code=98621)
    #school.delete_address_by_id(19)
    #school.delete_address_by_id(22)
    #school.update_address_by_id(23, 'testchangementaddress', 'test', 123456)
    #school.create_new_teacher(first_name='Mor', last_name='Diop', age=32, hiring_date=datetime.date(2025,8,5))
    #school.create_new_student('Theo', 'Sarhane', 12)

    #school.create_course(name="Programmation Python",start_date=datetime.date(2025,1,10),\
    #                    end_date=datetime.date(2025,1,19),id_teacher=3)

    school.print_all_database()


if __name__ == '__main__':
    main()
