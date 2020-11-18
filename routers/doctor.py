from fastapi import APIRouter, Depends, HTTPException
from dependencies.database import get_db
from dependencies.authentication import get_current_user_db_with_token
from sql_app import (shemas, models, crud)
from resources import strings
from starlette import status
from utils.token import Token
from validations.authentication import check_if_email_is_taken
router = APIRouter()


#here goes all the medic's code
@router.put(
    '/updatePassword', 
    dependencies=[Depends(get_db)]
    )
def update_password(doctor:shemas.MedicClave,token:str):
    current_user: models.Medico  = get_current_user_db_with_token(token)
    doctor_updated =  crud.update_password_doctor(current_user.id, doctor)
    if doctor_updated ==1:
        return {'ok': True, 
                'msg':strings.DOCTOR_UPDATED}
    else: 
       raise HTTPException(
           status_code=status.HTTP_304_NOT_MODIFIED,
           etail=strings.DOCTOR_NOT_UPDATED)


@router.put(
    '/updateEmailName', 
    dependencies=[Depends(get_db)]
    )
def update_password(doctor:shemas.MedicNombreCorreo,token:str):
    current_user: models.Medico  = get_current_user_db_with_token(token)
    if check_if_email_is_taken(current_user.id,doctor.correo):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= strings.USER_ALRRADY_REGISTERED)
    doctor_updated =  crud.update_password_doctor(current_user.id, doctor)
    if doctor_updated ==1:
        newToken = Token().encode(current_user.id,
                                  doctor.correo)
        return {'ok': True, 
                'msg':strings.DOCTOR_UPDATED,
                'token':newToken}
    else: 
       raise HTTPException(
           status_code=status.HTTP_304_NOT_MODIFIED,
           etail=strings.DOCTOR_NOT_UPDATED)
