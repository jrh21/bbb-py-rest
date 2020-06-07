# file to make the db file.
# it will clear any existing entries
from tinydb import TinyDB
from io_types import analogInTypes, analogOutTypes, digitalInTypes, digitalOutTypes

db = TinyDB('db/db.json')
db.truncate()

ai_table = db.table('ai_table')
ai_table.truncate()  # clear table if exiting

ao_table = db.table('ao_table')
ao_table.truncate()  # clear table if exiting

do_table = db.table('do_table')
do_table.truncate()  # clear table if exiting

di_table = db.table('di_table')
di_table.truncate()  # clear table if exiting

# build analogInTypes
for key, value in analogInTypes.items():
    ai_table.insert({'ioNum': key, 'gpio': value, 'val': 0})

# build analogOutTypes
for key, value in analogOutTypes.items():
    ao_table.insert({'ioNum': key, 'gpio': value, 'val': 0})

# build digitalInTypes
for key, value in digitalInTypes.items():
    di_table.insert({'ioNum': key, 'gpio': value, 'val': 0})

# build digitalOutTypes
for key, value in digitalOutTypes.items():
    do_table.insert({'ioNum': key, 'gpio': value, 'val': 0})
