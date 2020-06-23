
### to start
```
python3 app.py 
```

### install

https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/installation-on-ubuntu

On the bbb i had issues getting flask installed

```
pip install -U pip setuptools wheel
// install pip3 if needed
sudo apt install python3-pip 
pip3 install flask
```


```
sudo apt-get update
sudo apt-get install build-essential python-dev python-setuptools python-pip python-smbus -y
sudo pip install Adafruit_BBIO
```

Systemd script

Create unit file in /lib/systemd/system/you_service_name.service with the following content (as far as I can see your python script doesn't spawn new process while running, so Type should be simple. More info here):
```
nano /lib/systemd/system/bbio.service
sudo systemctl daemon-reload
sudo systemctl enable bbio.service
sudo service bbio start
sudo service bbio stop
sudo service bbio status

```



### for testing 
comment out all the `Adafruit_BBIO` libs 
and uncomment the random values as below ``val = random.uniform(0, 1)  # for testing``



```python
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
```


##### block port 5000

in ip tables -A is to add and -D is to delete an entry

```
// only allow localhost access to port 5000
sudo iptables -A INPUT -p tcp -s localhost --dport 5000 -j ACCEPT
// drop all other hosts
sudo  iptables -A INPUT -p tcp --dport 5000 -j DROP
// then save the tables
!!! Not tested
https://upcloud.com/community/tutorials/configure-iptables-centos/

// to remove a rule
sudo iptables -D INPUT -p tcp --dport 5000 -j DROP

```


### API for the GPIO

```
IO_TYPES
ui, uo, di, do

// read 
/read/IO_TYPE/IO_Number
// read all IOs as per type. like /read/all/ui
/read/all/IO_TYPE



```

#### Read a UI as a DI (jumper needs to be set to 10K)
off/open = around 0.9 vdc
on/closed = around 0.1 vdc



### read all
```
// read all DIs
http://0.0.0.0:5000/api/v1.0/read/all/di
// read all AIs
http://0.0.0.0:5000/api/v1.0/read/all/ai

```


#### UOs
https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/pwm

```
UOs 0 = 12vdc and 100 = 0vdc (Yes its backwards)
<io_num>/<val>/<pri>
uo/uo1/22/16
the priority (pri) is not supported yet but it's there for future use if needed
http://0.0.0.0:5000/api/v1.0/write/uo/uo1/100/16
// this returns the values that was stored in the DB (So not reading the actual pin value)

```


#### DOs
https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/gpio

```
/<io_num>/<val>/<pri>
the priority (pri) is not supported yet but it's there for future use if needed
DOs true for high false for low
http://0.0.0.0:5000/api/v1.0/write/do/do1/true/16


```

#### UIs
https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/adc

```
UIs will return a float between 0 and 1
http://0.0.0.0:5000/api/v1.0/read/ui/ui1

```


#### DIs
https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/gpio

```
DIs will return a int either 0 and 1 (0 is on 1 is off)
http://0.0.0.0:5000/api/v1.0/read/di/di1

```
