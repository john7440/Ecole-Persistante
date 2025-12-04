from dataclasses import dataclass
from typing import Optional, List

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

    def read_all(self) -> List[Student]:
        students: List[Student] = []
        try:
            with Dao.connection.cursor() as cursor:
                sql = "SELECT * FROM student s INNER JOIN person p ON s.id_person = p.id_person"
                cursor.execute(sql)
                records = cursor.fetchall()

            for record in records:
                student = Student(record['first_name'], record['last_name'],record['age'])
                student.id = record['student_nbr']

                students.append(student)

        except Exception as e:
            print(e)

        return students

    def update(self, student: Student) -> bool:
        """Met à jour en BD l'entité Student correspondant à student, pour y correspondre
        :param student: le student à mettre à jour
        :return: True si la mise à jour a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql= "UPDATE student SET first_name=%s, last_name=%s, age=%s WHERE id_student=%s"
                cursor.execute(sql, (student.first_name,student.last_name,student.age))
                Dao.connection.commit()
                return cursor.rowcount > 0

        except Exception as e:
            print(f"Erreur lors de la mise à jour su student: {e}")
            return False

    def delete(self, student: Student) -> bool:
        """Supprime en BD l'entité Student correspondant à student
        :param student: Le student à supprimer
        :return: True si la suppression a pu être réalisée
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql= "DELETE FROM student WHERE id_student=%s"
                cursor.execute(sql, (student.students_nb))
                Dao.connection.commit()
                return cursor.rowcount > 0

        except Exception as e:
            print(f"Erreur lors de la suppression de l'adresse: {e}")
            Dao.connection.rollback()
            return False


