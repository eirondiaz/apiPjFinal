from fastapi import FastAPI, HTTPException, Depends
import jwt
from sql_app import database, models, shemas
from dependencies.database import get_db
from fastapi import APIRouter

router = APIRouter()

@router.post(
    '/create',
    dependencies=[Depends(get_db)]
    )
def create_medico(med: shemas.Medic):
    try:
        medico = models.Medico(nombre = med.nombre, correo = med.correo, clave = med.clave)
        medico.save()
        return {'ok': True, 'msg': 'medico agregado'}
    except:
            raise HTTPException(status_code = 400, detail='ha ocurrido un error')
   