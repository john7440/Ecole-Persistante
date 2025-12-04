# -*- coding: utf-8 -*-

"""
Classe Dao[Course]
"""
from types import new_class

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
        try:
            with Dao.connection.cursor() as cursor:

                sql_check_teacher = "SElECT id_teacher from teacher WHERE id_teacher=%s"
                cursor.execute(sql_check_teacher,(course.id_teacher,))
                teacher_record = cursor.fetchone()

                if teacher_record is None:
                    print(f"Erreur: Aucun professeur trouvé avec l'id: {course.teacher}")
                    return 0

                sql_course = "INSERT INTO course (name, start_date, end_date, id_teacher) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql_course, (course.name,course.start_date,course.end_date,course.id_teacher))
                Dao.connection.commit()

                new_id = cursor.lastrowid
                course.id = new_id
                return new_id

        except Exception as e:
            print(f"Erreur lors de la création du cours: {e}")
            Dao.connection.rollback()
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

    @staticmethod
    def read_all() -> List[Course]:
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

    @staticmethod
    def read_all_with_teacher() -> List[Course]:
        """
        Renvoie la liste de tous les cours avec leur enseignant associé.

        :return: liste d'objets Course
        """
        courses: List[Course] = []
        try:
            with Dao.connection.cursor() as cursor:
                sql = """
                    SELECT c.id_course, c.name, c.start_date, c.end_date, c.id_teacher,
                           t.id_teacher, t.hiring_date, p.first_name, p.last_name
                    FROM course c
                    JOIN teacher t ON c.id_teacher = t.id_teacher
                    JOIN person p ON t.id_person = p.id_person
                """
                cursor.execute(sql)
                records = cursor.fetchall()

            for record in records:
                course = Course(
                    name=record['name'],
                    start_date=record['start_date'],
                    end_date=record['end_date'],
                    id_teacher=record['id_teacher']
                )
                course.id = record['id_course']

                # Optionnel : tu peux enrichir l’objet Course avec des infos sur le prof
                # par exemple en ajoutant un attribut teacher_name
                if hasattr(course, "teacher_name"):
                    course.teacher_name = f"{record['first_name']} {record['last_name']}"

                courses.append(course)

        except Exception as e:
            print(f"Erreur lors de la lecture des cours: {e}")

        return courses

    def update(self, course: Course) -> bool:
        """Met à jour en BD l'entité Course correspondant à course, pour y correspondre

        :param course: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = "UPDATE course SET name=%s, start_date=%s, end_date=%s WHERE id=%s"
                cursor.execute(sql, (course.name, course.start_date, course.end_date, course.id))
                Dao.connection.commit()
                return cursor.rowcount > 0

        except Exception as e:
            print(f"Le cours n'as pas pu être mis à jour: {e}")

    def delete(self, course: Course) -> bool:
        """Supprime en BD l'entité Course correspondant à course

        :param course: cours dont l'entité Course correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = "DELETE FROM course WHERE id_course=%s"
                cursor.execute(sql, (course.id,))
                Dao.connection.commit()
                return  cursor.rowcount > 0

        except Exception as e:
            print(f"Erreur lors de la suppression du cours: {e}")
            Dao.connection.rollback()
            return False

