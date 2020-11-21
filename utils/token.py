import jwt
from fastapi import HTTPException
from starlette import status
from resources import strings

class Token:
    SECRE_KEY  = 'JASLDJALSJDLAJSD342342LDALDALDNA343453454NDLANDLANDLasdasdas'
    ALGORITHM = 'HS256'
    def encode(self, user_id:int, user_email:str):
        user_dict:dict= {
            'user_id':user_id,
            'user_email':user_email
        }
        return jwt.encode(user_dict,self.SECRE_KEY,self.ALGORITHM)
    
    
    def decode(self, token:str):
        try:
            return jwt.decode(token,self.SECRE_KEY, self.ALGORITHM)
        except jwt.exceptions.DecodeError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=strings.UNATORIZED
                )