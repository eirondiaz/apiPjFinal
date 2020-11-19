from . import models, shemas
from peewee import fn, SQL

#sectio doctor-----------------------------------------------------------------------------------

#this is the doctor
def get_user_by_id(id:int):
    return models.Medico.get_or_none(models.Medico.id==id)

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
  
#sectio patients-----------------------------------------------------------------------------------
#TODO
def get_patients_total_visists_by_doctor(id_doctor:int):
    query = models.Paciente.select(
    models.Paciente,models.Consulta.select(
        fn.Count(models.Consulta).alias('_total_')).where(
            models.Consulta.paciente == models.Paciente.id)
    ).where(models.Paciente.medico ==id_doctor)
    pacients:list = []
    i = 0
    for pac in query:
        pacients.append(pac.__data__)
        pacients[i]['total_visit'] = pac.t3
        i = i +1  
    return pacients