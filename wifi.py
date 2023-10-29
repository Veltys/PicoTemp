#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''!
    wifi

    @file		: wifi.py
    @brief		: WiFi connector module

    @author		: Veltys
    @date		: 2023-10-29
    @version	: 1.0.0
    @usage		: (imported when needed)
    @note		: ...
'''


import network																	# Network management

from time import sleep															# Sleep function

class wifi:
    _password	= None
    _ssid		= None
    _wlan		= None


    def __init__(self, password = None, ssid = None):
        '''!
            Class constructor

            Initializes default values of the class

            @param leds					: List of three GPIO LEDs pins
            @param password				: WiFi network password
            @param ssid					: WiFi network SSID
        '''

        if(password != None):
            self._password = password

        if(ssid != None):
            self._ssid = ssid


    def connect(self):
        '''!
            Connects to the WiFi network

            @return						: Success of the connection
        '''
        
        if(self._ssid != None and self._password != None):
            self._wlan = network.WLAN(network.STA_IF)
            self._wlan.active(True)
            self._wlan.connect(self._ssid, self._password)

            # Wait for connect or fail
            max_wait = 10

            while(max_wait > 0):
                if(self._wlan.status() < 0 or self._wlan.status() >= 3):
                    break

                max_wait -= 1

                sleep(1)

            # Handle connection error
            if self._wlan.status() == 3:
                return True

            else:
                return False

        else:
            return False


    def disconnect(self):
        '''!
            Connection disconnector
        '''

        self._wlan.disconnect()
        self._wlan.active(False)


    def ip(self):
        '''!
            IP address observer

            @return						: Current IP address value
        '''

        if(self._wlan != None and self._wlan.status() == 3):
            return self._wlan.ifconfig()[0]

        else:
            return ''

