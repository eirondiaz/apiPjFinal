import peewee
from .database import db

        
class Medico(peewee.Model):
    id = peewee.IntegerField(primary_key=True)
    nombre = peewee.CharField()
    correo = peewee.CharField(unique=True)
    clave = peewee.CharField()

    class Meta:
        database = db
        
class Paciente(peewee.Model):
    id = peewee.IntegerField(primary_key=True)
    cedula = peewee.CharField(unique=True)
    nombre = peewee.CharField()
    apellido = peewee.CharField()
    foto = peewee.CharField()
    tipo_sangre = peewee.CharField()
    email = peewee.CharField()
    sexo = peewee.CharField()
    fecha_nac = peewee.CharField()
    alergias = peewee.CharField()
    medico = peewee.ForeignKeyField(Medico)

    class Meta:
        database = db