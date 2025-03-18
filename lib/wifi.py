#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''!
    wifi

    @file		: wifi.py
    @brief		: WiFi connector module

    @author		: Veltys
    @date		: 2025-03-17
    @version	: 1.2.0
    @usage		: (imported when needed)
    @note		: ...
'''


from time import sleep															# Sleep function

import network																	# Network management


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

        attempt = 0

        if(self._ssid != None and self._password != None):
            self._wlan = network.WLAN(network.STA_IF)
            self._wlan.active(True)

            while attempt < 3:
                max_wait = 30

                self._wlan.connect(self._ssid, self._password)

                while max_wait > 0:
                    status = self._wlan.status()

                    if(status < network.STAT_IDLE or status >= network.STAT_GOT_IP):
                        break

                    else:
                        max_wait -= 1

                        sleep(1)

                if self._wlan.isconnected():
                    break

                else:
                    attempt += 1

                    self._wlan.disconnect()

                    sleep(1)

            return self._wlan.status()

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

        if(self._wlan != None and self._wlan.status() == network.STAT_GOT_IP):
            return self._wlan.ifconfig()[0]

        else:
            return ''

