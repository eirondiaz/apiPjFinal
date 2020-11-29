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
#db = peewee.MySQLDatabase("dkabara_profinal", host="104.37.172.56", port=3306, user="dkabara_profinal", passwd="pro123final")
#DATABSE DE PHPMYADMIN
#db = peewee.MySQLDatabase("id15533455_progwebdb", host="https://databases-auth.000webhost.com/index.php", port=3306, user="id15533455_progwebdb2020", passwd="Progwebamadis.2020")
db = peewee.MySQLDatabase("sql9378992", host="sql9.freemysqlhosting.net", port=3306, user="sql9378992", passwd="b97kCrP7ci")
#db = peewee.MySQLDatabase("db_a6ab16_finalpr", host="mysql5034.site4now.net", port=3306, user="a6ab16_finalpr", passwd="admin123456")
db._state = PeeweeConnectionState()
