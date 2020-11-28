from fastapi import APIRouter, Depends, HTTPException
from dependencies.database import get_db
from dependencies.authentication import get_current_user_db_with_token
from sql_app import (shemas, models, crud)
from resources import strings
from starlette import status
from utils.token import Token
from validations.authentication import check_if_email_is_taken
from sql_app.shemas import ServerResponse
from datetime import datetime


router = APIRouter()

#here goes all the medic's code
@router.put(
    '/updatePassword', 
    dependencies=[Depends(get_db)]
    )
def update_password(doctor:shemas.MedicCambiarClave,token:str):
    current_user: models.Medico = get_current_user_db_with_token(token)
    if  not current_user.clave == doctor.clave:
        raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail=strings.INCORRECT_PASSWORD)
    doctor_updated =  crud.update_password_doctor(current_user.id, doctor.nueva_clave)
    if doctor_updated ==1:
        return ServerResponse(msg=strings.DOCTOR_UPDATED)
    else: 
       raise HTTPException(
           status_code=status.HTTP_304_NOT_MODIFIED,
           detail=strings.DOCTOR_NOT_UPDATED)


@router.put(
    '/updateEmailName', 
    dependencies=[Depends(get_db)]
    )
def update_email_name(doctor:shemas.MedicNombreCorreo,token:str):
    current_user: models.Medico  = get_current_user_db_with_token(token)
    if check_if_email_is_taken(doctor.correo):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= strings.USER_ALRRADY_REGISTERED)
    doctor_updated =  crud.update_email_name_doctor(current_user.id, doctor)
    if doctor_updated ==1:
        newToken = Token().encode(current_user.id,
                                  doctor.correo)
        return ServerResponse(msg=strings.DOCTOR_UPDATED, token=newToken)
    else: 
       raise HTTPException(
           status_code=status.HTTP_304_NOT_MODIFIED,
           detail=strings.DOCTOR_NOT_UPDATED)

@router.put(
    '/update', 
    dependencies=[Depends(get_db)]
    )
def update(doctor:shemas.MedicUpdate,token:str):
    current_user: models.Medico  = get_current_user_db_with_token(token)
    doctor_updated =  crud.update_doctor(current_user.id, doctor)
    if doctor_updated ==1:
        return ServerResponse(msg=strings.DOCTOR_UPDATED)
    else: 
       raise HTTPException(
           status_code=status.HTTP_304_NOT_MODIFIED,
           detail=strings.DOCTOR_NOT_UPDATED)
       
@router.put(
    '/updatePhoto', 
    dependencies=[Depends(get_db)]
    )
def update_photo(doctor:shemas.MedicFoto,token:str):
    current_user: models.Medico  = get_current_user_db_with_token(token)
    doctor_updated =  crud.update_photo(current_user.id, doctor)
    if doctor_updated ==1:
        return ServerResponse(msg=strings.DOCTOR_UPDATED)
    else: 
       raise HTTPException(
           status_code=status.HTTP_304_NOT_MODIFIED,
           detail=strings.DOCTOR_NOT_UPDATED)



@router.get(
    '/getCurrentDoctor',
    dependencies=[Depends(get_db)]
    )
def get_current_doctor(token:str):
    current_user: models.Medico  = get_current_user_db_with_token(token)
    current_user_dict:dict = {
        'nombre':current_user.nombre,
        'apellido':current_user.apellido,
        'pais':current_user.pais,
        'foto':current_user.foto,
        'correo':current_user.correo
    }
    return ServerResponse(msg=strings.SUCCESS, data=current_user_dict)


@router.get(
    '/getCurrentDoctorWithClossetConsults',
    dependencies=[Depends(get_db)]
    )
def get_current_doctor_with_(token:str):
    current_user: models.Medico  = get_current_user_db_with_token(token)
    consults =  crud.get_closset_consults_by_doctor(current_user.id)
    current_user_consults:dict = {
        'nombre':current_user.nombre,
        'apellido':current_user.apellido,
        'pais':current_user.pais,
        'foto':current_user.foto,
        'correo':current_user.correo
    }
    current_user_consults['fecha_hoy'] = datetime.today()
    current_user_consults['consults'] = consults
    if not consults:
        return ServerResponse(ok=False, 
                              msg=strings.NOT_COLSULTS, 
                              data=current_user_consults)
    return ServerResponse(msg=strings.SUCCESS, data=current_user_consults)




    