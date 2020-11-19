from fastapi import FastAPI, HTTPException, Depends
import jwt
from sql_app import database, models, shemas, crud
from dependencies.database import get_db
from dependencies.authentication import get_current_user_db_with_token
from fastapi import APIRouter
from resources import strings
from starlette import status

TOKEN_KEY = ''

router = APIRouter()

#metodos de paciente

#TODO
@router.get('/totalVisits', dependencies=[Depends(get_db)])
def get_total_visits(id_doctor):
    #THIS CODE IS GOINT TO IMPLEMENT LATER
    """ current_user:models.Medico = get_current_user_db_with_token(token)
    patients = crud.get_patients_total_visists_by_doctor(current_user.id) """
    patients:list = crud.get_patients_total_visists_by_doctor(id_doctor)
    if not patients:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=strings.NOT_PATIENTS
        )
    return{'ok': True, 
           'msg':strings.SUCCESS,
          'patients':patients}

#---------------------------------------------------------------------------------------------------

@router.post(
    '/create',
    dependencies=[Depends(get_db)]
    )
def create_paciente(token: str, pac: shemas.Patient):
    try:
        data = jwt.decode(token, TOKEN_KEY)
        try:
            med = models.Medico.get(models.Medico.id == data['id'])
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
        query = models.Paciente.select(models.Paciente).join(models.Medico).where(models.Medico.id == data['id'])
        pacienteList = []
        for pac in query:
            pacienteList.append(pac.__data__)

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
        return {'ok': True, 'paciente': pac.__data__}
    else:
        return {'ok': False, 'msg': 'no existe usuario'}

#ELIMINAR PACIENTE
@router.delete(
    '/{id}',
    dependencies=[Depends(get_db)]
)
def delete_pac(id: str):
    dela = models.Paciente.delete().where(models.Paciente.id == id).execute()
    if dela == 1:
        return {'ok': True, 'msg': 'paciente eliminado'}
    elif dela == 0:
        return {'ok': False, 'msg': 'no existe paciente con ese id'}

#EDITAR PACIENTE
@router.put(
    '/{id}',
    dependencies=[Depends(get_db)]
)
def update_pac(id: str, pac: shemas.Patient):
    updated = models.Paciente.update(**pac.dict()).where(models.Paciente.id == id).execute()
    if updated == 1:
        return {'ok': True, 'msg': 'paciente editado'}
    elif updated == 0:
        return {'ok': False, 'msg': 'error'}

