from fastapi import FastAPI
from peewee import SqliteDatabase, Model, IntegerField, CharField, DateTimeField, ForeignKeyField

db = SqliteDatabase('prueba.db')

class Medico(Model):
    id = IntegerField(primary_key=True)
    nombre = CharField()
    correo = CharField(unique=True)
    clave = CharField()

    class Meta:
        database = db

db.connect()
db.create_tables([Medico])

app = FastAPI()

@app.get('/')
def home():
    return 'funciona'