import jwt
from fastapi import HTTPException
from starlette import status
from resources import strings

class Token:
    SECRE_KEY  = ''
    """ ALGORITHM = 'HS256' """
    def encode(self, user_id:int, user_email:str):
        user_dict:dict= {
            'user_id':user_id,
            'user_email':user_email
        }
        return jwt.encode(user_dict,self.SECRE_KEY)
    
    
    def decode(self, token:str):
        try:
            return jwt.decode(token,self.SECRE_KEY)
        except jwt.exceptions.DecodeError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=strings.UNATORIZED
                )