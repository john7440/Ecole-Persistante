from dataclasses import dataclass
from typing import Optional

from ecole.daos.dao import Dao
from ecole.models.student import Student

@dataclass
class StudentDao(Dao[Student]):
    def create(self, student: Student) -> int:
        ...
        return 0

    def read(self, student_nbr: int) -> Optional[Student]:
        student: Optional[Student]

        with Dao.connection.cursor() as cursor:
            sql = ("SELECT * FROM person p INNER JOIN student s ON p.id_person = s.id_person WHERE s.student_nbr=%s")
            cursor.execute(sql, (student_nbr,))
            record = cursor.fetchone()
        if record is not None:
            student = Student(record['first_name'], record['last_name'],record['age'])
            student.id = record['student_nbr']
        else:
            student = None

        return student

    def update(self, student: Student) -> bool:
        """Met à jour en BD l'entité Course correspondant à course, pour y correspondre

        :param course: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        ...
        return True

    def delete(self, student: Student) -> bool:
        """Supprime en BD l'entité Course correspondant à course

        :param course: cours dont l'entité Course correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        ...
        return True

