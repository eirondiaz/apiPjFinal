from  sql_app import database
from fastapi import Depends
from sql_app.database import db_state_default


#this reset state from database and shouldn't export it to annother module or file
async def private_reset_db_state():
    database.db._state._state.set(db_state_default.copy())
    database.db._state.reset()

#dependency to export
#this open and close the connetion from db
def get_db(db_state=Depends(private_reset_db_state)):
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close()