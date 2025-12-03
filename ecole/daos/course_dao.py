# -*- coding: utf-8 -*-

"""
Classe Dao[Course]
"""

from ecole.models.course import Course
from ecole.daos.dao import Dao
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class CourseDao(Dao[Course]):
    def create(self, course: Course) -> int:
        """Crée en BD l'entité Course correspondant au cours course
        :param course: à créer sous forme d'entité Course en BD
        :return: l'id de l'entité insérée en BD, retourneras un message si erreur """
        ...
        return 0

    def read(self, id_course: int) -> Optional[Course]:
        """Renvoit le cours correspondant à l'entité dont l'id est id_course
           (ou None s'il n'a pu être trouvé)"""
        course: Optional[Course]
        
        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM course WHERE id_course=%s"
            cursor.execute(sql, (id_course,))
            record = cursor.fetchone()
        if record is not None:
            course = Course(record['name'], record['start_date'], record['end_date'])
            course.id = record['id_course']
        else:
            course = None

        return course

    def read_all(self) -> List[Course]:
        courses: List[Course] = []
        try:
            with Dao.connection.cursor() as cursor:
                sql = "SELECT * FROM course"
                cursor.execute(sql)
                records = cursor.fetchall()

            for record in records:
                course = Course(record['name'], record['start_date'], record['end_date'])
                course.id = record['id_course']

                courses.append(course)

        except Exception as e:
            print(f"Erreur lors de la lecture des cours: {e}")

        return courses


    def update(self, course: Course) -> bool:
        """Met à jour en BD l'entité Course correspondant à course, pour y correspondre

        :param course: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        ...
        return True

    def delete(self, course: Course) -> bool:
        """Supprime en BD l'entité Course correspondant à course

        :param course: cours dont l'entité Course correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        ...
        return True
