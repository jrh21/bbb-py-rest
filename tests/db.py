from tinydb import TinyDB, Query

db = TinyDB('db.json')
# db.insert({'1_state': "writeOk", '2_ioNum': "DO1", '3_gpio': "P8_7", '4_val': 0, '5_msg': "wrote value to the GPIO"})
# db.insert({'ioNum': "DO1", 'gpio': "P8_7", 'val': 0})
do_table = db.table('do_table')
# do_table.insert({'ioNum': "DO1", 'gpio': "P8_7", 'val': 0})
IO_DB = Query()

# do_table.update({'val': 22}, IO_DB.ioNum == 'DO1')

result = do_table.get(Query()['ioNum'] == 'DO1')
x = result.get("val")
print(x)
