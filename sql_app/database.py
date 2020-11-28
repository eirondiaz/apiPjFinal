import peewee
from contextvars import ContextVar
#from playhouse.mysql_ext import MySQLConnectorDatabase


DATABASE_NAME = "prueba.db"

db_state_default = {"closed": None, "conn": None, "ctx": None}
db_state = ContextVar("db_state", default=db_state_default.copy())

class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]

#"check_same_thread" is going to do delete it later

#db = peewee.SqliteDatabase(DATABASE_NAME, check_same_thread=False)
#db = peewee.MySQLDatabase("db_a6ab16_finalpr", host="mysql5034.site4now.net", port=3306, user="a6ab16_finalpr", passwd="admin123456")
db = peewee.MySQLDatabase("finalProyect",
                          host="mysql-16036-0.cloudclusters.net", 
                          port=16036, user="pfinal",
                          passwd="123456789")

db._state = PeeweeConnectionState()
