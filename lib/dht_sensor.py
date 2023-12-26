#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''!
    dht_sensor

    @file		: dht_sensor.py
    @brief		: Generic DHT11/22 sensor manager module

    @author		: Veltys
    @date		: 2023-12-18
    @version	: 2.0.0
    @usage		: (imported when needed)
    @note		: ...
'''


class dht_sensor:
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

            else:
                self._temperature = self._sensor.temperature()
                self._humidity = self._sensor.humidity()


    def temperature(self):
        '''!
            _temperature variable observer

            @return						: Variable value
        '''

        return self._temperature
