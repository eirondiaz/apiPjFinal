from sql_app import crud, models


def check_if_email_is_taken(email:str):
    user:models.Medico = crud.get_user_by_email(email)
    if user:
        return True
    return False