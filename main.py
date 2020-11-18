from fastapi import FastAPI
from routers import doctor, patient,authentication, consulta
from sql_app import database, models

database.db.connect()
database.db.create_tables([models.Paciente, models.Medico, models.Consulta])
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
    doctor.router,
    prefix="/doctor",
    tags=["doctor"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    patient.router,
    prefix="/patient",
    tags=["patient"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    consulta.router,
    prefix="/consulta",
    tags=["consulta"],
    responses={404: {"description": "Not found"}},
)

@app.get('/')
def home():
    return 'api del proyecto final de Prog Web'
