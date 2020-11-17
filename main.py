from fastapi import FastAPI, HTTPException, Depends
import jwt
from sql_app import database, models, shemas
from dependencies.database import get_db
from routers import medic, patient,authentication


database.db.connect()
database.db.create_tables([models.Paciente, models.Medico])
database.db.close()

TOKEN_KEY = ''

app = FastAPI()

app.include_router(
    authentication.router,
    prefix="/authentication",
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    medic.router,
    prefix="/medic",
    tags=["medic"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    patient.router,
    prefix="/patient",
    tags=["patient"],
    responses={404: {"description": "Not found"}},
)

@app.get('/')
def home():
    return 'funciona'
