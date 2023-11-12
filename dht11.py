#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''!
    dht11

    @file		: dht11.py
    @brief		: DHT11 sensor manager module

    @author		: Veltys
    @date		: 2023-11-07
    @version	: 1.0.2
    @usage		: (imported when needed)
    @note		: ...
'''


from dht import DHT11
from machine import Pin


class dht11:
    _humidity = None
    _sensor = None
    _temperature = None


    def __init__(self, pin = None):
        '''!
            Class constructor

            Initializes default values of the class

            @param pin					: GPIO sensor pin
        '''

        if(pin != None):
            self.sensor(pin)


    def humidity(self):
        '''!
            _humidity variable observer

            @return						: Variable value
        '''

        return self._humidity


    def measure(self):
        '''!
            Measures temperature and humidity
        '''

        if(self._sensor != None):
            try:
                self._sensor.measure()

            except Exception:
                self._temperature = None
                self._humidity = None

            except OSError:
                self._temperature = None
                self._humidity = None

            else:
                self._temperature = self._sensor.temperature()
                self._humidity = self._sensor.humidity()


    def sensor(self, pin):
        '''!
            Configures the sensor

            @param pin					: GPIO sensor pin
        '''

        self._sensor = DHT11(Pin(int(pin)))


    def temperature(self):
        '''!
            _temperature variable observer

            @return						: Variable value
        '''

        return self._temperature
