# PiGps - Self Hosted GPS Route Recording

This repo hosts code which powers a self hosted GPS route recorder (something
like Strava).

## Hardware

Theoretically you should be able to run this on any kind of micro-computer
and NMEA GPS chip, however I use the following hardware:

* [Raspberry Pi Zero W](https://www.adafruit.com/product/3708?gclid=Cj0KCQjwv5uKBhD6ARIsAGv9a-x8D0DkOuW-BhM-yR9fFZPOeCFhJ9wJL7zyDUUeN9hV10AE2AZCCX4aAjvwEALw_wcB)
* [Neo 6M GPS Module](https://www.amazon.com/Microcontroller-Compatible-Sensitivity-Navigation-Positioning/dp/B07P8YMVNT)
* [Solar Powered Portable Power Source](https://www.amazon.com/30000mAh-Portable-Flashlight-Waterproof-Compatible/dp/B095W3JVQ4)

## Running

To start the recoding process run:

```
python3 gps-record.py
```

When you are done you can kill the recording process. To view the route you just
recorded run the web server:

```
flask run --host=0.0.0.0
```

and then navigate to the IP address/hostname of the Pi:

```
http://<pi>:5000
```
