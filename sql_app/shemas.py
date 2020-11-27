from pydantic import BaseModel
from typing import Optional , List
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
    
class MedicApellido(BaseModel):
    apellido:Optional[str] = None
    
class MedicPais(BaseModel):
    pais:Optional[str] = None
    
class MedicProfesion(BaseModel):
    profesion:Optional[str] = None

class MedicFoto(BaseModel):
    foto:Optional[str] = None

class MedicClave(BaseModel):
    clave: Optional[str] = None
    
class MedicCambiarClave(MedicClave):
    nueva_clave:str

class MedicCorreo(BaseModel):
    correo: Optional[str] = None
    
class MedicNombre(BaseModel):
    nombre: Optional[str] = None
    
                  
class MedicUpdate(MedicNombre,
                  MedicApellido, 
                  MedicPais,
                  MedicProfesion):
    pass

class Medic(MedicClave, 
            MedicCorreo, 
            MedicNombre,
            MedicFoto,
            MedicPais,
            MedicProfesion,
            MedicApellido):
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


class PatientId(BaseModel):
    id_patient:int
        

class Consult(BaseModel):
    nota: Optional[str] = None
    monto: Optional[float] = None
    motivo: Optional[str] = None
    no_seguro: Optional[str] = None
    diagnostico: Optional[str] = None
    foto_evidencia: Optional[str] = None
    fecha: Optional[datetime] = None

class ConsultCreate(Consult):
    id_paciente:int
    pass

