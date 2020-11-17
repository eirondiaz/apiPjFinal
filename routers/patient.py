from fastapi import FastAPI, HTTPException, Depends
import jwt
from sql_app import database, models, shemas
from dependencies.database import get_db
from fastapi import APIRouter

TOKEN_KEY = ''

router = APIRouter()

#metodos de paciente
@router.post(
    '/create',
    dependencies=[Depends(get_db)]
    )
def create_paciente(token: str, pac: shemas.Patient):
    try:
        data = jwt.decode(token, TOKEN_KEY)
        try:
            med = models.Medico.get(models.Medico.id == data['id'])
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
            paciente = models.Paciente.create(**pac.dict(), medico = med)
            return {'ok': True, 'msg': 'paciente registrado'}
        except:
            raise HTTPException(status_code = 400, detail='error')
    except jwt.exceptions.DecodeError:
            return {'ok': False, 'msg': 'token invalido'}
            
        
#funciones de paciente
#OBTENER TODOS LOS PACIENTES
@router.get(
    '/patients',
    dependencies=[Depends(get_db)]
    )
def get_all_patient(token: str):
    try:
        data = jwt.decode(token, TOKEN_KEY)
        query = models.Paciente.select(models.Paciente).join
        (models.Medico).where(models.Medico.id == data['id'])
        pacienteList = []
        for pac in query:
            pacienteList.append(pac._data_)

        return {'ok': True, 'pacientes': pacienteList}
    except jwt.exceptions.DecodeError:
        return {'ok': False, 'msg': 'token invalido'}
    
    
#OBTENER PACIENTE POR ID
@router.get(
    '/{id}',
    dependencies=[Depends(get_db)]
    )
def get_pac_by_id(id: int):
    pac = models.Paciente.get_or_none(models.Paciente.id == id)
    if pac:
        return {'ok': True, 'paciente': pac}
    else:
        return {'ok': False, 'msg': 'no existe usuario'}
