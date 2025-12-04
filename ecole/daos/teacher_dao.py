from dataclasses import dataclass
from typing import Optional, List

from ecole.daos.dao import Dao
from ecole.models.teacher import Teacher

@dataclass
class TeacherDao(Dao[Teacher]):
    def create(self, teacher: Teacher) -> int:
        """
        Crée en BD un nouveau professeur.
        - Insère d'abord la personne dans la table `person`
        - Puis insère le professeur dans la table `teacher`
        :param teacher: entité Teacher à insérer
        :return: l'id du professeur inséré (0 si échec)
        """
        try:
            with Dao.connection.cursor() as cursor:

                sql_person = "INSERT INTO person (first_name, last_name, age) VALUES (%s, %s, %s)"
                cursor.execute(sql_person, (teacher.first_name, teacher.last_name, teacher.age))
                person_id = cursor.lastrowid

                sql_teacher = "INSERT INTO teacher (hiring_date, id_person) VALUES (%s, %s)"
                cursor.execute(sql_teacher, (teacher.hiring_date, person_id))
                Dao.connection.commit()

                new_id = cursor.lastrowid
                teacher.id = new_id
                return new_id

        except Exception as e:
            print(f"Erreur lors de la création du professeur: {e}")
            Dao.connection.rollback()
            return 0

    def read(self, id_teacher: int) -> Optional[Teacher]:
        """Retourne un teacher en fonction de son id"""
        teacher: Optional[Teacher]

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM teacher t INNER JOIN person p ON t.id_person = p.id_person WHERE t.id_teacher=%s"
            cursor.execute(sql, (id_teacher,))
            record = cursor.fetchone()
        if record is not None:
            teacher = Teacher(record['first_name'], record['last_name'],record['age'], record['hiring_date'])
            teacher.id = record['id_teacher']
        else:
            teacher = None

        return teacher

    def read_all(self) -> List[Teacher]:
        """Renvoi tous les teachers"""
        teachers: List[Teacher] = []
        try:
            with Dao.connection.cursor() as cursor:
                sql = "SELECT * FROM teacher t INNER JOIN person p ON t.id_person = p.id_person"
                cursor.execute(sql)
                records = cursor.fetchall()

            for record in records:
                teacher = Teacher(record['first_name'], record['last_name'],record['age'], record['hiring_date'])
                teacher.id = record['id_teacher']

                teachers.append(teacher)

        except Exception as e:
            print(f"Erreur lors de la lecture des cours: {e}")

        return teachers

    def update(self, teacher: Teacher) -> bool:
        """Met à jour en BD l'entité Teacher correspondant à teacher, pour y correspondre
        :param teacher: Le teacher a update
        :return: True si la mise à jour a pu être réalisée sinon False
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = "UPDATE teacher SET first_name=%s, last_name=%s, age=%S, hiring_date=%s WHERE id_teacher=%s"
                cursor.execute(sql,(teacher.first_name, teacher.last_name, teacher.age, teacher.hiring_date, teacher.id))
                Dao.connection.commit()
                return cursor.rowcount > 0

        except Exception as e:
            print(f"Le professeur n'as pas pu être mis a jour : {e}")
            return False

    def delete(self, teacher: Teacher) -> bool:
        """Supprime en BD l'entité Teacher correspondant à teacher
        :param teacher: Teacher à supprimer
        :return: True si la suppression a pu être réalisée sinon False
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = "DELETE FROM teacher WHERE id_teacher=%s"
                cursor.execute(sql, (teacher.id,))
                Dao.connection.commit()
                return cursor.rowcount > 0

        except Exception as e:
            print(f"Erreur lors de la suppression du professeur: {e}")
            Dao.connection.rollback()
            return False

