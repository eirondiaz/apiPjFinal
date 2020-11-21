from pydantic import BaseModel
from typing import Optional 
from datetime import datetime 

class ServerResponse:
    def __init__(self, ok:bool = True,msg:str ='', token:str = '', data = ''):
       self.ok = ok
       self.msg = msg
       self.token = token
       self.data = data
    ok:bool
    msg:str
    token:str
    data =''


class MedicClave(BaseModel):
    clave: Optional[str] = None

class MedicCorreo(BaseModel):
    correo: Optional[str] = None
    
class MedicNombre(BaseModel):
    nombre: Optional[str] = None

class Medic(MedicClave, MedicCorreo, MedicNombre):
    pass

class MedicNombreCorreo(MedicNombre, MedicCorreo):
    pass

class MedicLogin(MedicClave, MedicCorreo):
    pass


class PatientFechaNacimiento(BaseModel):
    fecha_nac: Optional[datetime] = None

class Patient(PatientFechaNacimiento):
    cedula: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    foto: Optional[str] = None
    tipo_sangre: Optional[str] = None
    email: Optional[str] = None
    sexo: Optional[str] = None
    alergias: Optional[str] = None
    fecha_nac: Optional[datetime] = None


class Consult(BaseModel):
    nota: Optional[str] = None
    monto: Optional[str] = None
    motivo: Optional[str] = None
    no_seguro: Optional[str] = None
    diagnostico: Optional[str] = None
    foto_evidencia: Optional[str] = None
    fecha: Optional[datetime] = None

class ConsultCreate(Consult):
    id_paciente:int
    pass

