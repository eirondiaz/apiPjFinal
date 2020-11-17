from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from peewee import SqliteDatabase, Model, IntegerField, CharField, DateTimeField, ForeignKeyField
import jwt

db = SqliteDatabase('prueba.db')

class Medic(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[str] = None
    clave: Optional[str] = None

class Medico(Model):
    id = IntegerField(primary_key=True)
    nombre = CharField()
    correo = CharField(unique=True)
    clave = CharField()

    class Meta:
        database = db

class Patient(BaseModel):
    cedula: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    foto: Optional[str] = None
    tipo_sangre: Optional[str] = None
    email: Optional[str] = None
    sexo: Optional[str] = None
    fecha_nac: Optional[str] = None
    alergias: Optional[str] = None

class Paciente(Model):
    id = IntegerField(primary_key=True)
    cedula = CharField(unique=True)
    nombre = CharField()
    apellido = CharField()
    foto = CharField()
    tipo_sangre = CharField()
    email = CharField()
    sexo = CharField()
    fecha_nac = CharField()
    alergias = CharField()
    medico = ForeignKeyField(Medico)

    class Meta:
        database = db

db.connect()
db.create_tables([Medico, Paciente])

app = FastAPI()

@app.get('/')
def home():
    return 'funciona'

#metodos de medico
@app.post('/medico')
def create_medico(med: Medic):
    try:
        medico = Medic(nombre = med.nombre, correo = med.correo, clave = med.clave)
        medico.save()
        return {'ok': True, 'msg': 'medico agregado'}
    except:
        raise HTTPException(status_code = 400, detail='ha ocurrido un error')

#metodos de paciente
@app.post('/paciente')
def create_paciente(token: str, pac: Patient):
    try:
        data = jwt.decode(token, '''aqui va el key''')
        try:
            med = Medico.get(Medico.id == data['id'])
            '''paciente = Paciente.create(
                        cedula = pac.cedula,
                        nombre = pac.nombre,
                        apellido = pac.apellido,
                        sexo = pac.sexo,
                        foto = pac.foto,
                        tipo_sangre = pac.tipo_sangre,
                        email = pac.email,
                        fecha_nac = pac.fecha_nac,
                        alergias = pac.alergias,
                        medico = med
                        )'''
            paciente = Paciente.create(**pac.dict())
            return {'ok': True, 'msg': 'paciente registrado'}
        except:
            raise HTTPException(status_code = 400, detail='error')
    except jwt.exceptions.DecodeError:
            return {'ok': False, 'msg': 'token invalido'}