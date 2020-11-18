from utils.token import Token
from fastapi import HTTPException
from starlette import status
from sql_app import crud
from resources import strings

def get_current_user_db_with_token(token:str =''):
    token_dict:dict = Token().decode(token)
    current_user= crud.get_user_by_id(token_dict['id'])
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=strings.USER_NOT_FOUND
            )
    return current_user