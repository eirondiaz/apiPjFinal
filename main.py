from fastapi import FastAPI
from routers import doctor, patient,authentication, consulta
from sql_app import database, models

database.db.connect()
database.db.create_tables([models.Paciente, models.Medico, models.Consulta])
database.db.close()

app = FastAPI()

def routers(file, prefix:str, tags:str):
    app.include_router(
    file.router,
    prefix= f"/{prefix}",
    tags=[f"{tags}"],
    responses={404: {"description": "Not found"}},)

routers(authentication,'authentication','authentication')
routers(doctor,'doctor','doctor')
routers(patient,'patient','patient')
routers(consulta,'consulta','consulta')

@app.get('/')
def home():
    return 'api del proyecto final de Prog Web'
