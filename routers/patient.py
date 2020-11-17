from fastapi import FastAPI, HTTPException, Depends
import jwt
from sql_app import database, models, shemas
from dependencies.database import get_db
from fastapi import APIRouter

router = APIRouter()

#metodos de paciente
@router.post(
    '/create',
    dependencies=[Depends(get_db)]
    )
def create_paciente(token: str, pac: shemas.Patient):
    try:
        data = jwt.decode(token, '''aqui va el key''')
        try:
            med = models.Medico.get(Medico.id == data['id'])
            '''paciente = Paciente.create(
                        cedula = pac.cedula,
                        nombre = pac.nombre,
                        apellido = pac.apellido,
                        sexo = pac.sexo,
                        foto = pac.foto,
                        tipo_sangre = pac.tipo_sangre,
                        email = pac.email,
                        fecha_nac = pac.fecha_nac,
                        alergias = pac.alergias,
                        medico = med
                        )'''
            paciente = models.Paciente.create(**pac.dict())
            return {'ok': True, 'msg': 'paciente registrado'}
        except:
            raise HTTPException(status_code = 400, detail='error')
    except jwt.exceptions.DecodeError:
            return {'ok': False, 'msg': 'token invalido'}