from fastapi import FastAPI, HTTPException, Depends
from sql_app import database, models, shemas, crud
from dependencies.database import get_db
from dependencies.authentication import get_current_user_db_with_token
from fastapi import APIRouter
from starlette import status
from utils.token import Token
from resources import strings
from sql_app.shemas import ServerResponse

router = APIRouter()

#OBTENER TODAS LAS CONSULTAS
@router.get(
    '/',
    dependencies=[Depends(get_db)]
)
def get_all_consultas(token: str):
    current_user:models.Medico = get_current_user_db_with_token(token)
    query = models.Consulta.get_or_none(models.Consulta.medico == current_user.id)
    if not query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
                      detail=strings.NOT_COLSULTS)
    return ServerResponse(msg=strings.SUCCESS,data= query.__data__)


#OBTENER CONSULTA POR ID
@router.get(
    '/{id}',
    dependencies=[Depends(get_db)]
)
def get_consulta_by_id(id: int, token):
    current_user:models.Medico = get_current_user_db_with_token(token)
    consult = crud.get_consulta_by_id_by_doctor(current_user.id, id)
    if not consult:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= strings.CONSULT_NOT_FOUND)
    else:
        return ServerResponse(msg=strings.SUCCESS, data=consult.__data__)


#EDITAR CONSULTA
@router.put(
    '/{id_consult}',
    dependencies=[Depends(get_db)]
)
def edit_consulta(id_consult,con: shemas.Consult, token):
    current_user:models.Medico = get_current_user_db_with_token(token)
    edited = models.Consulta.update(**con.dict()).where(
        models.Consulta.id == id_consult, models.Consulta.medico==current_user.id
        ).execute()
    if edited == 1:
        return ServerResponse(msg=strings.CONSULT_UPDATED)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=strings.COULD_NOT_UPDATE)

#ELIMINAR CONSULTA
@router.delete(
    '/{id_consult}',
    dependencies=[Depends(get_db)]
)
def delete_consulta(id_consult: str, token):
    current_user:models.Medico = get_current_user_db_with_token(token)
    dela = models.Consulta.delete().where(
        models.Consulta.id == id_consult,
        models.Consulta.medico==current_user.id).execute()
    if dela == 1:
        return ServerResponse(msg=strings.CONSULT_DELETED)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=strings.COULD_NOT_DELETE)

@router.post(
    '/create',
    dependencies=[Depends(get_db)]
    )
def create_cosulta(consulta:shemas.ConsultCreate, token:str):
    current_user:models.Medico = get_current_user_db_with_token(token)
    try:
        crud.create_consulta(consulta, id_doctor=current_user.id)
        return ServerResponse(msg=strings.CREATED)
    except:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail= strings.CONSULT_NOT_CREATED 
            )
        
