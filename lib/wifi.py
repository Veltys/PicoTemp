#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''!
    wifi

    @file		: wifi.py
    @brief		: WiFi connector module

    @author		: Veltys
    @date		: 2025-03-18
    @version	: 1.4.0
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


    def isconnected(self):
        '''!
            Connection checker

            Checks if the device is connected to the WiFi network

            @return                     : True if connected, False otherwise
        '''

        return self._wlan.isconnected()


    def get_rssi(self):
        '''!
            RSSI observer

            Gets the Received Signal Strength Indicator (RSSI) of the connected WiFi network

            @return                     : The RSSI value in dBm if connected, None otherwise
        '''

        res = None

        if self.isconnected():
            try:
                res = self._wlan.status('rssi')

            except (AttributeError, OSError):
                res = None

        else:
            res = None

        return res


    @staticmethod
    def signal_bars(rssi, total_bars):
        '''!
            Converts WiFi signal strength (RSSI) to a number of signal bars

            This method maps the RSSI value (in dBm) to a signal strength representation
            using a given number of bars

            - RSSI values typically range from `-30 dBm` (excellent signal) to `-90 dBm` (very weak signal)
            - If `rssi` falls outside this range, the function returns `total_bars` as an error indicator
            - Otherwise, the method scales the RSSI within `0` to `total_bars - 1`

            @param rssi                 : WiFi signal strength in dBm
            @param total_bars           : Maximum number of bars to represent the signal strength

            @return                     : An integer (`0` to `total_bars - 1`) representing the number of bars,
                                          or `-1` in case of an out-of-range value
        '''

        RSSI_MAX = -30                                                          # Excellent signal
        RSSI_MIN = -90                                                          # Poor signal

        if(rssi >= RSSI_MIN and rssi <= RSSI_MAX):
            # Map RSSI to the number of bars (scaling between RSSI_MIN and RSSI_MAX)
            bars = round((rssi - RSSI_MIN) / (RSSI_MAX - RSSI_MIN) * (total_bars - 1))

        else:
            bars = -1

        return bars
