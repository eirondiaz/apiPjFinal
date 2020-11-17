from fastapi import FastAPI, HTTPException, Depends
import jwt
from sql_app import database, models, shemas
from dependencies.database import get_db
from fastapi import APIRouter

router = APIRouter()

TOKEN_KEY = ''

#REGISTRO DE MEDICO
@router.post(
    '/register',
    dependencies=[Depends(get_db)]
    )
def create_medico(med: shemas.Medic):
    try:
        medico = models.Medico(nombre = med.nombre, correo = med.correo, clave = med.clave)
        medico.save()
        return {'ok': True, 'msg': 'medico agregado'}
    except:
            raise HTTPException(status_code = 400, detail='ha ocurrido un error')

#LOGIN DE MEDICO
@router.post(
    '/login',
    dependencies=[Depends(get_db)]
    )
def login(med: shemas.MedicLogin):
    medico = models.Medico.get_or_none(models.Medico.correo == med.correo and models.Medico.clave == med.clave)
    if medico == None:
        return {'ok': False, 'msg': 'correo o clave invalido'}
    else:
        token = jwt.encode({'id': medico.id}, TOKEN_KEY)
        return {'ok': True, 'token': token}
   