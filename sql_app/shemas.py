from pydantic import BaseModel
from typing import Optional  

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

class Consult(BaseModel):
    nota: Optional[str] = None
    monto: Optional[str] = None
    motivo: Optional[str] = None
    no_seguro: Optional[str] = None
    diagnostico: Optional[str] = None
    foto_evidencia: Optional[str] = None

class ConsultCreate(Consult):
    id_paciente:int
    pass