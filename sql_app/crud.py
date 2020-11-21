from . import models, shemas
from peewee import fn, SQL
from datetime import datetime

#sectio doctor-----------------------------------------------------------------------------------

#this is the doctor
#not implemet yet
def get_user_by_id(id:int):
    return models.Medico.get_or_none(models.Medico.id==id)

def get_user_by_email(email:str):
    return models.Medico.get_or_none(models.Medico.correo==email)

def update_password_doctor(id:int, doctor_password:shemas.MedicClave):
    docotor_udated =  models.Medico.update(
        **doctor_password.dict()).where(models.Medico.id == id).execute()
    return docotor_udated
    
def update_email_name_doctor(id:int, doctor_name_email:shemas.MedicNombreCorreo):
    docotor_udated =  models.Medico.update(
        **doctor_name_email.dict()).where(models.Medico.id == id).execute()
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