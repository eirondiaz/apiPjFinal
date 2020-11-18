from fastapi import FastAPI, HTTPException, Depends
from sql_app import database, models, shemas
from dependencies.database import get_db
from fastapi import APIRouter
from utils.token import Token

router = APIRouter()

#OBTENER TODAS LAS CONSULTAS
@router.get(
    '/',
    dependencies=[Depends(get_db)]
)
def get_all_consultas(tokenn: str):
    data = Token().decode(tokenn)
    query = models.Consulta.select(models.Consulta, models.Paciente).join(models.Medico).where(models.Medico.id == data['id'])
    consultList = []
    for con in query:
        consultList.append(con.__data__)

    return {'ok': True, 'consultas': consultList}

#OBTENER CONSULTA POR ID
@router.get(
    '/{id}',
    dependencies=[Depends(get_db)]
)
def get_consulta_by_id(id: str):
    query = models.Consulta.get_or_none(models.Consulta.id == id)
    if query == None:
        return {'ok': False, 'msg': 'consulta no encontrada'}
    else:
        return {'ok': True, 'consulta': query.__data__}

#EDITAR CONSULTA
@router.put(
    '/{id}',
    dependencies=[Depends(get_db)]
)
def edit_consulta(id: str, con: shemas.Consult):
    edited = models.Consulta.update(**con.dict()).where(models.Consulta.id == id).execute()
    if edited == 1:
        return {'ok': True, 'msg': 'consulta editada'}
    elif edited == 0:
        return {'ok': False, 'msg': 'error'}

#ELIMINAR CONSULTA
@router.delete(
    '/{id}',
    dependencies=[Depends(get_db)]
)
def delete_consulta(id: str):
    dela = models.Consulta.delete().where(models.Consulta.id == id).execute()
    if dela == 1:
        return {'ok': True, 'msg': 'consulta eliminada'}
    elif dela == 0:
        return {'ok': False, 'msg': 'error'}
