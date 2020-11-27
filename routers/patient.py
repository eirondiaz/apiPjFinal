from fastapi import FastAPI, HTTPException, Depends
import jwt
from sql_app import database, models, shemas, crud
from dependencies.database import get_db
from dependencies.authentication import get_current_user_db_with_token
from fastapi import APIRouter
from resources import strings
from starlette import status
from datetime import datetime
from sql_app.shemas import ServerResponse
from typing import List

router = APIRouter()

#metodos de paciente
#TODO
""" @router.get(
    '/getBytotalVisits', 
    dependencies=[Depends(get_db)]
    )
def get_total_visits(token):
    current_user:models.Medico = get_current_user_db_with_token(token)
    patients:list = crud.get_patients_total_visists_by_doctor(current_user.id)
    if not patients:
        return ServerResponse(ok=False,
                              msg=strings.NOT_PATIENTS,
                              data=[])
    return ServerResponse(msg=strings.SUCCESS, data=patients) """
    
#TODO
@router.get(
    '/getByBirthdate/{patiente_birthdate}',
    dependencies=[Depends(get_db)]
    )
def get_patients_by_birthdate(patiente_birthdate:datetime, token):
    current_user:models.Medico = get_current_user_db_with_token(token)
    patients:list = crud.get_patients_by_date_by_doctor(
        current_user.id, patiente_birthdate
        )
    if not patients:
        return ServerResponse(ok=False,
                              msg=strings.NOT_PATIENTS,
                              data=[])
    return ServerResponse(msg=strings.SUCCESS, data=patients)



#ELIMINAR MULTIPLES PACIENTES
@router.delete(
    '/deleteMultiple',
    dependencies=[Depends(get_db)]
)
def delete_multiple(patients: List[shemas.PatientId], token):
    current_user:models.Medico = get_current_user_db_with_token(token)
    try:
        data =  crud.delete_multiple_patients_by_doctor(current_user.id, patients)
    except: 
        raise HTTPException(status_code=status.HTTP_409_CONFLICT
                            ,detail=strings.ERROR)
    return ServerResponse(msg=strings.SUCCESS)

#---------------------------------------------------------------------------------------------------

@router.post(
    '/create',
    dependencies=[Depends(get_db)]
    )
def create_paciente(pac: shemas.Patient, token: str):
    current_user:models.Medico = get_current_user_db_with_token(token)
    try:
        paciente = models.Paciente.create(
            **pac.dict(), medico = current_user.id)
        return ServerResponse(msg=strings.PATIENT_ADED)
    except:
        raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail= strings.PATIENT_NOT_CREATED 
        )

#TODO    
#funciones de paciente
#OBTENER TODOS LOS PACIENTES
""" @router.get(
    '/patients',
    dependencies=[Depends(get_db)]
    )
def get_all_patient(token: str):
    current_user:models.Medico = get_current_user_db_with_token(token)
    query = models.Paciente.select(models.Paciente).where(
        models.Paciente.medico == current_user.id)
    pacienteList = []
    for pac in query:
        pacienteList.append(pac.__data__)
    if not pacienteList:
            return ServerResponse(ok=False,
                              msg=strings.NOT_PATIENTS,
                              data=[])
    return ServerResponse(data=pacienteList, msg=strings.SUCCESS)
        
     """
    
@router.get(
    '/patients',
    dependencies=[Depends(get_db)]
    )
def get_all_patient_with_total_visits(token: str):
    current_user:models.Medico = get_current_user_db_with_token(token)
    patients:list = crud.get_patients_total_visists_by_doctor(current_user.id)
    if not patients:
        return ServerResponse(ok=False,
                              msg=strings.NOT_PATIENTS,
                              data=[])
    return ServerResponse(msg=strings.SUCCESS, data=patients)
    
#OBTENER PACIENTE POR ID
@router.get(
    '/{id_patient}',
    dependencies=[Depends(get_db)]
    )
def get_pac_by_id(id_patient: int, token):
    current_user:models.Medico = get_current_user_db_with_token(token)
    pac = models.Paciente.get_or_none(
        models.Paciente.id == id_patient, 
        models.Paciente.medico == current_user.id)
    if pac:
        return ServerResponse(msg=strings.SUCCESS, data=pac.__data__ )
    else:
        return ServerResponse(ok=False,
                              msg=strings.NOT_PATIENTS,
                              data={})


#ELIMINAR PACIENTE
@router.delete(
    '/{id_patient}',
    dependencies=[Depends(get_db)]
)
def delete_pac(id_patient: str, token):
    current_user:models.Medico = get_current_user_db_with_token(token)
    dela = models.Paciente.delete().where(
        models.Paciente.id == id_patient,
        models.Paciente.medico == current_user.id).execute()
    if dela == 1:
        return ServerResponse(msg=strings.PATIENT_DELETED)
    else:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail= strings.PATIENT_NOT_DELETED)

#EDITAR PACIENTE
@router.put(
    '/{id_patient}',
    dependencies=[Depends(get_db)]
)
def update_pac(id_patient: str, pac: shemas.Patient, token):
    current_user:models.Medico = get_current_user_db_with_token(token)
    updated = models.Paciente.update(**pac.dict()).where(
        models.Paciente.id == id_patient, 
        models.Paciente.medico ==current_user.id).execute()
    if updated == 1:
        return ServerResponse(msg=strings.PATIENT_UPDATED)
    else:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail= strings.PATIENT_NOT_UPDATED)
