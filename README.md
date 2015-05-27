
This is a very simple script that posts data to a sensor and pulls from its control chanel using Sense Tecnic's IoT platform and an Intel Edison board.

Dependencies
================

* Python >2.7
* Wiringx86 (https://github.com/emutex/wiring-x86)


Getting Started
===============

You will need to create a WoTKit account at https://wotkit.sensetecnic.com

You can generate a key and password at: http://wotkit.sensetecnic.com/wotkit/keys.

You can create a sensor to receive the data at: http://wotkit.sensetecnic.com/wotkit/sensors

Edit the wotkit_demo.py file and modify the following lines to match your credentials and sensor name:

```
SENSOR_NAME = 'YOURSENSORNAME'
USERNAME = 'YOURUSERNAME'
PASSWORD = 'YOURPASSWORD'
```

Wiring Up
=========

To wire a sensor (e.g. a temp sensor):

![alt](https://raw.githubusercontent.com/SenseTecnic/wotkit-example-python-edison/master/diagram-sensor_bb.png)

To wire a 5V relay:

![alt](https://raw.githubusercontent.com/SenseTecnic/wotkit-example-python-edison/master/diagram-relay_bb.png)

Running Script
================

To run the script run:

```
python wotkit-edison.py
```

Running at Boot on Edison
=========================

Edison uses systemd for services, we have provided a file ```wotkit-edison.service``` that will run the shell script if located at ```/home/root/wotkit-example-python-edison/startwotkitedison.sh```.

So, first, make that file executable:


```
cd /home/root/wotkit-example-python-edison
chmod a+x startwotkitedison.sh
```

Copy the service file to the ```lib/systemd/system``` folder.


```
cd /home/root/wotkit-example-python-edison
cp wotkit-edison.service /lib/systemd/system/wotkit-edison.service
```

And now reload systemd and try to restart your service:


```
systemctl daemon-reload
systemctl start wotkit-edison.service
```

If everything is alright you should get no errors. If you want to configure it to start at boot enable it like so:

```
 systemctl enable wotkit-edison.service

```

Now reboot and see if everything is alright.
