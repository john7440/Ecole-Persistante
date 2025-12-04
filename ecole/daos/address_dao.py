from ecole.daos.dao import Dao
from ecole.models.address import Address
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class AddressDao(Dao[Address]):
    def create(self, address: Address) -> int:
        """Crée en BD l'entité Course correspondant au cours course

        :param course: à créer sous forme d'entité Course en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        try:
            with Dao.connection.cursor() as cursor:
                sql = "INSERT INTO address (street,city, postal_code) VALUES (%s, %s, %s)"
                cursor.execute(sql, (address.street, address.city, address.postal_code))
                Dao.connection.commit()
                new_id = cursor.lastrowid
                address.id = new_id
                return new_id
        except Exception as e:
            print(f"Erreur lors de la création de l'adresse: {e}")
            Dao.connection.rollback()
            return 0

    def read(self, id_address: int) -> Optional[Address]:
        """Renvoit le cours correspondant à l'entité dont l'id est id_course
           (ou None s'il n'a pu être trouvé)"""
        address: Optional[Address]

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM address a WHERE a.id_address=%s"
            cursor.execute(sql, (id_address,))
            record = cursor.fetchone()
        if record is not None:
            address = Address(record['street'], record['city'], record['postal_code'])
            address.id = record['id_address']
        else:
            address = None

        return address

    def read_all(self) -> List[Address]:
        addresses: List[Address] = []
        try:
            with Dao.connection.cursor() as cursor:
                sql = "SELECT * FROM address"
                cursor.execute(sql)
                records = cursor.fetchall()

            for record in records:
                address = Address(record['street'], record['city'], record['postal_code'])
                address.id = record['id_address']

                addresses.append(address)

        except Exception as e:
            print(f"Erreur lors de la lecture des adresses: {e}")

        return addresses

    def update(self, address: Address) -> bool:
        """Met à jour en BD l'entité Course correspondant à course, pour y correspondre

        :param course: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        ...
        return True

    def delete(self, address: Address) -> bool:
        """Supprime en BD l'entité Course correspondant à course

        :param course: cours dont l'entité Course correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        ...
        return True