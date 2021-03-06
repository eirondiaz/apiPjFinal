from . import models, shemas
from peewee import fn, SQL
from datetime import datetime
from typing import List
from datetime import datetime



#sectio doctor-----------------------------------------------------------------------------------

#this is the doctor
#not implemet yet
def get_user_by_id(id:int):
    return models.Medico.get_or_none(models.Medico.id==id)


def get_user_by_email(email:str):
    return models.Medico.get_or_none(models.Medico.correo==email)

def update_password_doctor(id:int, new_password:str):
    docotor_udated =  models.Medico.update(
        clave= new_password).where(models.Medico.id == id).execute()
    return docotor_udated
    
def update_email_name_doctor(id:int, doctor_name_email:shemas.MedicNombreCorreo):
    docotor_udated =  models.Medico.update(
        **doctor_name_email.dict()).where(models.Medico.id == id).execute()
    return docotor_udated

def update_doctor(id:int,doctor_profesion_contry:shemas.MedicUpdate):
    docotor_udated =  models.Medico.update(
        **doctor_profesion_contry.dict()).where(models.Medico.id == id).execute()
    return docotor_udated

def update_photo(id:int,doctor_photo:shemas.MedicFoto):
    docotor_udated =  models.Medico.update(
    **doctor_photo.dict()).where(models.Medico.id == id).execute()
    return docotor_udated


#sectio cosulta-----------------------------------------------------------------------------------

def create_consulta(consulta: shemas.ConsultCreate, id_doctor:int):
    models.Consulta.create(**consulta.dict(), 
                           medico= id_doctor, 
                           paciente= consulta.id_paciente)
  

def get_consulta_with_patient_by_id(id_doctor:int, id_consulta:int):
    consult = models.Consulta.select(models.Consulta, models.Paciente).join(
        models.Paciente).where(
            models.Consulta.id==id_consulta,
            models.Consulta.medico==id_doctor
            )
    i:int = 0
    consult_list:list = []
    for target_list in consult:
        consult_list.append(target_list.__data__)
        consult_list[i]['paciente'] = target_list.paciente.__data__
        i = i +1
    return consult_list


def get_closset_consults_by_doctor(id_doctor:int):
    consults = models.Consulta.select(models.Consulta).where(
        models.Consulta.fecha>datetime.today(), models.Consulta.medico == id_doctor
        ).order_by(models.Consulta.fecha.asc()).limit(6)
    consult_list:list = []
    for target_list in consults:
        consult_list.append(target_list.__data__)
    return consult_list


def get_all_consults_by_doctor(id_doctor:int):
    consults = models.Consulta.select(models.Consulta).where(
        models.Consulta.medico == id_doctor
        ).order_by(models.Consulta.fecha.desc())
    consult_list:list = []
    for target_list in consults:
        consult_list.append(target_list.__data__)
    return consult_list
    
def get_all_consults_by_date_by_doctor(id_doctor:int, date:datetime):
    consults = models.Consulta.select(models.Consulta, models.Paciente).join(
        models.Paciente).where(
        models.Consulta.medico == id_doctor, models.Consulta.fecha == date
        ).order_by(models.Consulta.fecha.desc())
    consults_list:list = []
    i:int = 0 
    for target_list in consults:
        consults_list.append(target_list.__data__)
        consults_list[i]['paciente'] = target_list.paciente.__data__
        i = i +1
    return consults_list
    
  
#sectio patients-----------------------------------------------------------------------------------

def get_patients_total_visists_by_doctor(id_doctor:int):
    query = models.Paciente.select(
    models.Paciente,models.Consulta.select(
        fn.Count(models.Consulta.paciente).alias('_total_')).where(
            models.Consulta.paciente == models.Paciente.id)
    ).where(models.Paciente.medico ==id_doctor)
    patients:list = []
    i = 0
    for pat in query:
        patients.append(pat.__data__)
        patients[i]['total_visit'] = pat.t3
        i = i +1  
    return patients


def get_patients_by_date_by_doctor(id_doctor:int, birthdate:datetime):
    query = models.Paciente.select(
        models.Paciente).where(models.Paciente.fecha_nac==birthdate,
                               models.Paciente.medico== id_doctor)
    patients:list = []
    for pat in query:
        patients.append(pat.__data__)
    return patients


def delete_multiple_patients_by_doctor(id_doctor, patients_id:List[shemas.PatientId]):
    for target_list in patients_id:
        models.Paciente.delete().where(
            models.Paciente.id==target_list.id_patient,
            models.Paciente.medico==id_doctor ).execute()
        