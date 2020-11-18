from . import models, shemas

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
    