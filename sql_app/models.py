import peewee
from .database import db
from datetime import datetime

        
class Medico(peewee.Model):
    id = peewee.AutoField(primary_key=True)
    nombre = peewee.CharField()
    apellido = peewee.CharField()
    profesion  = peewee.CharField()
    pais = peewee.CharField()
    foto = peewee.TextField()
    correo = peewee.CharField(unique=True)
    clave = peewee.CharField()

    class Meta:
        database = db
        
class Paciente(peewee.Model):
    id = peewee.AutoField(primary_key=True)
    cedula = peewee.CharField(index=True)
    nombre = peewee.CharField()
    apellido = peewee.CharField()
    foto = peewee.TextField()
    tipo_sangre = peewee.CharField()
    email = peewee.CharField()
    sexo = peewee.CharField()
    fecha_nac = peewee.DateTimeField(default=datetime.now())
    alergias = peewee.CharField()
    medico = peewee.ForeignKeyField(Medico)

    class Meta:
        database = db

class Consulta(peewee.Model):
    id = peewee.AutoField(primary_key=True)
    nota = peewee.CharField()
    monto = peewee.FloatField()
    fecha = peewee.DateTimeField(default=datetime.now())
    motivo = peewee.CharField()
    no_seguro = peewee.CharField()
    diagnostico = peewee.CharField()
    foto_evidencia = peewee.TextField()
    medico = peewee.ForeignKeyField(Medico)
    paciente = peewee.ForeignKeyField(Paciente)

    class Meta:
        database = db