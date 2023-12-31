#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''!
    dht11

    @file		: dht11.py
    @brief		: DHT11 sensor manager module

    @author		: Veltys
    @date		: 2023-12-18
    @version	: 2.0.0
    @usage		: (imported when needed)
    @note		: ...
'''


from dht import DHT11
from dht_sensor import dht_sensor
from machine import Pin


class dht11(dht_sensor):
    _humidity = None
    _sensor = None
    _temperature = None


    def sensor(self, pin):
        '''!
            Configures the sensor

            @param pin					: GPIO sensor pin
        '''

        self._sensor = DHT11(Pin(int(pin)))
