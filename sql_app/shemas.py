from pydantic import BaseModel
from typing import Optional  

class Medic(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[str] = None
    clave: Optional[str] = None

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