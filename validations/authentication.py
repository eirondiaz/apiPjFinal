from sql_app import crud, models


def check_if_email_is_taken(idUser:int, email:str):
    user:models.Medico = crud.get_user_by_id(idUser)
    if user.correo == email:
        return True
    return False