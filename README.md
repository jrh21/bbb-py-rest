
### to start
```
python3 app.py 
```

### install

https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/installation-on-ubuntu

On the bbb i had issues getting flask installed

```
pip install -U pip setuptools wheel
pip3 install flask
```


```
sudo apt-get update
sudo apt-get install build-essential python-dev python-setuptools python-pip python-smbus -y
sudo pip install Adafruit_BBIO
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




### API calls

#### UOs
https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/pwm

```
UOs 0 = 0vdc and 100 = 12vdc
http://0.0.0.0:5000/api/v1.0/write/uo/uo1/100

```


#### DOs
https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/gpio

```
DOs true for high false for low
http://0.0.0.0:5000/api/v1.0/write/do/do1/true

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