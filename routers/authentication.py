from fastapi import FastAPI, HTTPException, Depends
import jwt
from sql_app import database, models, shemas
from dependencies.database import get_db
from fastapi import APIRouter
from utils.token import Token
from validations.authentication import check_if_email_is_taken
from starlette import status
from resources import strings
from sql_app.shemas import ServerResponse

router = APIRouter()

#REGISTRO DE MEDICO
@router.post(
    '/register',
    dependencies=[Depends(get_db)]
    )
def create_medico(med: shemas.MedicRegister):
    if check_if_email_is_taken(med.correo):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= strings.USER_ALRRADY_REGISTERED)
    try:
        medico:models.Medico = models.Medico(**med.dict())
        medico.save()
        token = Token().encode(medico.id,medico.correo)
        return ServerResponse(
            msg=strings.DOCTOR_ADED,token = token)
    except:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail=strings.ERROR)

#LOGIN DE MEDICO
@router.post(
    '/login',
    dependencies=[Depends(get_db)]
    )
def login(med: shemas.MedicLogin):
    medico:models.Medico = models.Medico.get_or_none(
        models.Medico.correo == med.correo, 
        models.Medico.clave == med.clave)
    if not medico:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=strings.USER_OR_EMAIL_NOT_FOUND)
    else:
        token =Token().encode(user_id=medico.id, user_email=medico.correo)
        return ServerResponse(msg=strings.LOGGED, token=token)
   