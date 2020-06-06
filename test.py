# import random
#
# print(bool(random.getrandbits(1)))
# print(random.uniform(0,1))
import random

from func import command_to_bool, is_float, analog_in, analog_out, digital_in, digital_out
from io_types import analogInTypes, analogOutTypes, digitalInTypes, digitalOutTypes

io_num = 'UO1'

gpio = analog_out(io_num)
# print(gpio)

# analogInTypes

# print(analogInTypes)
# print(analogInTypes.keys())
# print(analogInTypes.values())
# print(analogInTypes.items())
#
# x = analogInTypes.get("P9_39")
# print(x)

case_list = {}
val = random.uniform(0, 1)  # for testing
for key, value in analogInTypes.items():
    print(value)
    # case = {key: value, key: value, key:val }
    # case_list[key] = case
print(case_list)

# from tinydb import TinyDB, Query
#
# # db.insert({'1_state': "writeOk", '2_ioNum': "DO1", '3_gpio': "P8_7", '4_val': 0, '5_msg': "wrote value to the GPIO"})
# # db.insert({'ioNum': "DO1", 'gpio': "P8_7", 'val': 0})
#
# # do_table.insert({'ioNum': "DO1", 'gpio': "P8_7", 'val': 0})
#
#
# db = TinyDB('db.json')
# do_table = db.table('do_table')
# IO_DB = Query()
# # do_table.update({'val': 22}, IO_DB.ioNum == 'DO1')
#
# for key, value in analogInTypes.items():
#     do_table.insert({'ioNum': key, 'gpio': value, 'val': 0})


