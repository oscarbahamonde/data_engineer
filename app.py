#1.1 Se resuelve el problema utilizando la libreria SQLModel
#1.2 Se recomienda parsear todos los id de la capa origen a un dato uuid4 para evitar duplicados, en la capa staging se puede utilizar esta librería para validar la calidad de los datos

from pyspark import F
from sqlmodel import SQLModel, create_engine, Field
from datetime import date

db = create_engine('mysql+pymysql://user:password@db:3306/db')

class Cliente(SQLModel, table=True):
    codpersona: str = Field(primary_key=True, min_length=14,
                            max_length=20, nullable=False)
    nombre: str = Field(min_length=8, max_length=100, nullable=False)
    apellido: str = Field(min_length=7, max_length=100, nullable=False)
    fnac: date = Field(nullable=False, max_length="8")
    correo: str = Field(nullable=False, max_length="130")

    @classmethod
    def post_from_txt(cls):
        with open('words.txt') as txt:
            matrix = [line.split() for line in txt]
            for row in matrix:
                if cls.query.filter_by(codpersona=row[0]).first() is None:
                    cls.insert(
                        codpersona=row[0], nombre=row[1], apellido=row[2], fnac=row[3], correo=row[4])
                elif cls.query.filter_by(codpersona=row[0]).first() is not None:
                    cls.update(
                        codpersona=row[0], nombre=row[1], apellido=row[2], fnac=row[3], correo=row[4])

SQLModel.metadata.create_all(db)

if '__init__' == '__main__':
    Cliente.post_from_txt()
