from dataclasses import dataclass
from typing import Optional, List

from ecole.daos.dao import Dao
from ecole.models.teacher import Teacher

@dataclass
class TeacherDao(Dao[Teacher]):
    def create(self, teacher: Teacher) -> int:
        ...
        return 0

    def read(self, id_teacher: int) -> Optional[Teacher]:
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
        """Met à jour en BD l'entité Course correspondant à course, pour y correspondre

        :param course: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        ...
        return True

    def delete(self, teacher: Teacher) -> bool:
        """Supprime en BD l'entité Course correspondant à course

        :param course: cours dont l'entité Course correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        ...
        return True

