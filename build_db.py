from tinydb import TinyDB, Query
from io_types import analogInTypes, analogOutTypes, digitalInTypes, digitalOutTypes
db = TinyDB('db.json')
ai_table = db.table('ai_table')
ao_table = db.table('ao_table')
do_table = db.table('do_table')
di_table = db.table('di_table')
IO_DB = Query()

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


