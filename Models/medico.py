from pydantic import BaseModel
from typing import Optional

class Medic(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[str] = None
    clave: Optional[str] = None