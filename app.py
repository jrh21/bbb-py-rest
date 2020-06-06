#!flask/bin/python

# rest server
import random
from tinydb import TinyDB, Query
from flask import Flask, jsonify, make_response
from func import command_to_bool, is_float, analog_in, analog_out, digital_in, digital_out
from io_types import analogInTypes, analogOutTypes, digitalInTypes, digitalOutTypes

app = Flask(__name__)

# DB for persisting data
db = TinyDB('db.json')
ai_table = db.table('ai_table')
ao_table = db.table('ao_table')
do_table = db.table('do_table')
di_table = db.table('di_table')
IO_DB = Query()

# #
# # bbb gpio lib
# import Adafruit_BBIO.GPIO as GPIO
# import Adafruit_BBIO.PWM as PWM
# import Adafruit_BBIO.GPIO as GPIO
# import Adafruit_BBIO.ADC as ADC
#
# # DOs
# GPIO.setup("P8_7", GPIO.OUT)
# GPIO.setup("P8_8", GPIO.OUT)
# GPIO.setup("P8_9", GPIO.OUT)
# GPIO.setup("P8_10", GPIO.OUT)
# GPIO.setup("P8_12", GPIO.OUT)
# GPIO.setup("P9_29", GPIO.OUT)
# GPIO.setup("P9_12", GPIO.OUT)
#
# # UOs
# # UOs 0 = 0vdc and 100 = 12vdc
# # PWM.start("P9_14", 0, 1000, 1) // for startup
# # PWM.set_duty_cycle("P9_14", 0) //write 0v
# # PWM.set_duty_cycle("P9_14",100) //write 12v
# #
# PWM.start("P8_13", 0, 1000, 1)  # for startup
# PWM.start("P9_14", 0, 1000, 1)
# PWM.start("P9_21", 0, 1000, 1)
# PWM.start("P9_42", 0, 1000, 1)
# PWM.start("P8_19", 0, 1000, 1)
# PWM.start("P9_16", 0, 1000, 1)
# PWM.start("P9_22", 0, 1000, 1)
#
# # DIs
# GPIO.setup("P9_30", GPIO.IN)
# GPIO.setup("P9_15", GPIO.IN)
# GPIO.setup("P9_31", GPIO.IN)
# GPIO.setup("P9_28", GPIO.IN)
# GPIO.setup("P9_23", GPIO.IN)
# GPIO.setup("P9_25", GPIO.IN)
# GPIO.setup("P9_27", GPIO.IN)
#
# # AIs
# ADC.setup()

# api stuff
api_ver = 'v1.0'  # change version number as needed
uo = 'uo'
ui = 'ui'
do = 'do'
di = 'di'

# http messages
http_error = 404
http_success = 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), http_error)


## index page
@app.route('/', methods=['GET'])
def index_page(io_num=None, val=None):
    return jsonify({'1_state': "whats up"}), http_success


## WRITE DOs
@app.route('/api/' + api_ver + '/write/' + do + '/<io_num>/<val>', methods=['GET'])
def write_outputs_do(io_num=None, val=None):
    gpio = digital_out(io_num)
    io_num = io_num.upper()
    val = command_to_bool(val)
    print(val)
    if gpio == -1:
        return jsonify({'1_state': "unknownType", '2_ioNum': io_num, '3_gpio': gpio, '4_val': val,
                        '5_msg': digitalOutTypes}), http_error
    elif val is True:
        # GPIO.output(gpio, GPIO.HIGH)
        do_table.update({'val': int(val)}, IO_DB.gpio == gpio)
        return jsonify({'1_state': "writeOk", '2_ioNum': io_num, '3_gpio': gpio, '4_val': int(val),
                        '5_msg': 'wrote value to the GPIO'}), http_success
    elif val is False:
        # GPIO.output(gpio, GPIO.LOW)
        do_table.update({'val': int(val)}, IO_DB.gpio == gpio)
        return jsonify({'1_state': "writeOk", '2_ioNum': io_num, '3_gpio': gpio, '4_val': int(val),
                        '5_msg': 'wrote value to the GPIO'}), http_success
    else:
        return jsonify({'1_state': "unknownValue", '2_ioNum': io_num, '3_gpio': gpio, '4_val': val,
                        '5_msg': 'value must be a boolean an int an string 1/0 or string on/off'}), http_error


## WRITE AOs

@app.route('/api/' + api_ver + '/write/' + uo + '/<io_num>/<val>', methods=['GET'])
def write_outputs_ao(io_num=None, val=None):
    gpio = analog_out(io_num)
    io_num = io_num.upper()
    if gpio == -1:
        return jsonify({'1_state': "unknownType", '2_ioNum': io_num, '3_gpio': gpio, '4_val': val,
                        "5_msg": analogOutTypes}), http_error
    elif is_float(val):
        val = float(val)
        if 0 <= val <= 100:
            # PWM.set_duty_cycle(gpio, val)
            ao_table.update({'val': val}, IO_DB.gpio == gpio)
            return jsonify({'1_state': "writeOk", '2_ioNum': io_num, '3_gpio': gpio, '4_val': val,
                            '5_msg': 'wrote value to the GPIO'}), http_success
        else:
            return jsonify({'1_state': "unknownRange", '2_ioNum': io_num, '3_gpio': gpio, '4_val': val,
                            '5_msg': 'val must be >=0 and <=100'}), http_success
    else:
        return jsonify({'1_state': "unknownValue", '2_ioNum': io_num, '3_gpio': gpio, '4_val': val,
                        '5_msg': 'value must be a float'}), http_error


# READ DOs

@app.route('/api/' + api_ver + '/read/' + do + '/<io_num>', methods=['GET'])
def read_do(io_num=None):
    gpio = digital_out(io_num)
    io_num = io_num.upper()
    if gpio == -1:
        return jsonify({'1_state': "unknownType", '2_ioNum': io_num, '3_gpio': gpio, '4_val': 'null',
                        "5_msg": digitalOutTypes}), http_error
    else:
        result = do_table.get(Query()['gpio'] == gpio)
        val = result.get("val")
        return jsonify({'1_state': "readOk", '2_ioNum': io_num, '3_gpio': gpio, '4_val': val,
                        '5_msg': 'read value ok'}), http_success


# READ AOs

@app.route('/api/' + api_ver + '/read/' + uo + '/<io_num>', methods=['GET'])
def read_ao(io_num=None):
    gpio = analog_out(io_num)
    io_num = io_num.upper()
    if gpio == -1:
        return jsonify({'1_state': "unknownType", '2_ioNum': io_num, '3_gpio': gpio, '4_val': 'null',
                        "5_msg": digitalOutTypes}), http_error
    else:
        result = ao_table.get(Query()['gpio'] == gpio)
        val = result.get("val")
        return jsonify({'1_state': "readOk", '2_ioNum': io_num, '3_gpio': gpio, '4_val': val,
                        '5_msg': 'read value ok'}), http_success


# READ DIs

@app.route('/api/' + api_ver + '/read/' + di + '/<io_num>', methods=['GET'])
def read_di(io_num=None):
    gpio = digital_in(io_num)
    if gpio == -1:
        return jsonify({'1_state': "unknownType", '2_ioNum': io_num, '3_gpio': gpio, '4_val': 'null',
                        "5_msg": digitalInTypes}), http_error
    else:
        # val = GPIO.input(gpio)
        val = bool(random.getrandbits(1))  # for testing
        val = int(val)  # for testing
        return jsonify({'1_state': "readOk", '2_ioNum': io_num, '3_gpio': gpio, '4_val': val,
                        '5_msg': 'read value ok'}), http_success


#  READ UIs

@app.route('/api/' + api_ver + '/read/' + ui + '/<io_num>', methods=['GET'])
def read_ai(io_num=None):
    gpio = analog_in(io_num)
    if gpio == -1:
        return jsonify({'1_state': "unknownType", '2_ioNum': io_num, '3_gpio': gpio, '4_val': 'null',
                        "5_msg": analogInTypes}), http_error
    else:
        # val = ADC.read(gpio)
        val = random.uniform(0, 1)  # for testing
        return jsonify({'1_state': "readOk", '2_ioNum': io_num, '3_gpio': gpio, '4_val': val,
                        '5_msg': 'read value ok'}), http_success


# READ ALL DIs

@app.route('/api/' + api_ver + '/read/all/' + di, methods=['GET'])
def read_di_all():
    case_list = random.uniform(0, 1)  # for testing
    # case_list = {}
    # for key, value in digitalInTypes.items():
    #     case = {"val": GPIO.input(value)}
    #     case_list[key] = case

    return jsonify({'1_state': "readOk", '2_ioNum': "all", '3_gpio': "all", '4_val': case_list,
                    '5_msg': 'read DIs ok'}), http_success


# READ ALL UIs

@app.route('/api/' + api_ver + '/read/all/' + ui, methods=['GET'])
def read_ai_all():
    case_list = random.uniform(0, 1)  # for testing
    # case_list = {}
    # for key, value in analogInTypes.items():
    #     case = {"val": ADC.read(value)}
    #     case_list[key] = case
    return jsonify({'1_state': "readOk", '2_ioNum': "all", '3_gpio': "all", '4_val': case_list,
                    '5_msg': 'read UIs ok'}), http_success


# READ DOs

@app.route('/api/' + api_ver + '/read/all/' + do, methods=['GET'])
def read_do_all(io_num=None):
    gpio = digital_out(io_num)
    io_num = io_num.upper()
        val = do_table.get(Query()['gpio'] == gpio)
        return jsonify({'1_state': "readOk", '2_ioNum': io_num, '3_gpio': gpio, '4_val': val,
                        '5_msg': 'read value ok'}), http_success



if __name__ == '__main__':
    app.run(host='0.0.0.0')
