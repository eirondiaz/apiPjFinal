from pydantic import BaseModel
from typing import Optional  

class MedicClave(BaseModel):
    clave: Optional[str] = None

class MedicCorreo(BaseModel):
    correo: Optional[str] = None

class Medic(MedicClave, MedicCorreo):
    nombre: Optional[str] = None
   
class MedicLogin(MedicClave, MedicCorreo):
    pass


class Patient(BaseModel):
    cedula: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    foto: Optional[str] = None
    tipo_sangre: Optional[str] = None
    email: Optional[str] = None
    sexo: Optional[str] = None
    fecha_nac: Optional[str] = None
    alergias: Optional[str] = None