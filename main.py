from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from peewee import SqliteDatabase, Model, IntegerField, CharField, DateTimeField, ForeignKeyField, IntegrityError
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

TOKEN_KEY = ''

app = FastAPI()

@app.get('/')
def home():
    return 'api para el proyecto final de Prog Web'

#funciones de medico
#REGISTRO DE MEDICO
@app.post('/medico')
def registrar(med: Medic):
    try:
        medico = Medico(nombre = med.nombre, correo = med.correo, clave = med.clave)
        medico.save()
        return {'ok': True, 'msg': 'medico agregado'}
    except:
        raise HTTPException(status_code = 400, detail='error')

#LOGIN DE MEDICO
@app.post('/medico/login')
def login(med: Medic):
    medico = Medico.get_or_none(Medico.correo == med.correo and Medico.clave == med.clave)
    if medico == None:
        return {'ok': False, 'msg': 'correo o clave invalido'}
    else:
        token = jwt.encode({'id': medico.id}, TOKEN_KEY)
        return {'ok': True, 'token': token}

#funciones de paciente
#OBTENER TODOS LOS PACIENTES
@app.get('/paciente')
def get_all_patient(token: str):
    try:
        data = jwt.decode(token, TOKEN_KEY)

        query = Paciente.select(Paciente).join(Medico).where(Medico.id == data['id'])
        pacienteList = []
        for pac in query:
            pacienteList.append(pac.__data__)

        return {'ok': True, 'pacientes': pacienteList}
    except jwt.exceptions.DecodeError:
        return {'ok': False, 'msg': 'token invalido'}

#OBTENER PACIENTE POR ID
@app.get('/paciente/{id}')
def get_pac_by_id(id: str):
    pac = Paciente.get_or_none(Paciente.id == id)
    if pac == None:
        return {'ok': True, 'paciente': pac.__data__}
    else:
        return {'ok': False, 'msg': 'no existe usuario'}

#CREAR PACIENTE
@app.post('/paciente')
def create_paciente(token: str, pac: Patient):
    try:
        data = jwt.decode(token, TOKEN_KEY)
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