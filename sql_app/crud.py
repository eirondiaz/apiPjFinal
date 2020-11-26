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

def update_contry_profesion_doctor(id:int,doctor_profesion_contry:shemas.MedicProfesionPais):
    docotor_udated =  models.Medico.update(
        **doctor_profesion_contry.dict()).where(models.Medico.id == id).execute()
    return docotor_udated
#sectio cosulta-----------------------------------------------------------------------------------

def create_consulta(consulta: shemas.ConsultCreate, id_doctor:int):
    models.Consulta.create(**consulta.dict(), 
                           medico= id_doctor, 
                           paciente= consulta.id_paciente)
  
def get_consulta_by_id_by_doctor(id_doctor:int, id_consulta:int):
    consult = models.Consulta.get_or_none(
        models.Consulta.id == id_consulta, models.Consulta.medico==id_doctor)
    return consult


def get_closset_consults_by_doctor(id_doctor:int):
    consults = models.Consulta.select(models.Consulta).where(
        models.Consulta.fecha>datetime.today(), models.Consulta.medico == id_doctor
        ).order_by(models.Consulta.fecha.asc()).limit(6)
    consult_list:list = []
    for target_list in consults:
        consult_list.append(target_list.__data__)
    return consult_list
    
  
#sectio patients-----------------------------------------------------------------------------------

def get_patients_total_visists_by_doctor(id_doctor:int):
    query = models.Paciente.select(
    models.Paciente,models.Consulta.select(
        fn.Count(models.Consulta).alias('_total_')).where(
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
        