#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''!
    leds

    @file		: leds.py
    @brief		: LEDs manager module

    @author		: Veltys
    @date		: 2023-10-29
    @version	: 1.0.0
    @usage		: (imported when needed)
    @note		: ...
'''


from time import sleep
import errno                                                                    # Error codes
import sys                                                                      # System-specific parameters and functions

from machine import Pin															# GPIO pins management
import utime																	# Microtime-related functions

try:
    from config import config                                                   # Configuration

except ImportError:
    print('Error: Config file not found', file = sys.stderr)
    sys.exit(errno.ENOENT)


class leds:
    _leds		= None


    def __init__(self, leds = None):
        '''!
            Class constructor

            Initializes default values of the class

            @param leds					: List of three GPIO LEDs pins
        '''

        if(leds != None):
            self.leds(leds)


    def blink(self, led, time, threaded = False):
        '''!
            LED blinker

            @param led					: LED to blink
            @param time					: Duration of the blinking
            @param threaded				: Enables thread management
        '''

        internal_led	= int(led)
        internal_time	= int(time)

        if(self._leds != None and internal_led < 3 and internal_time > 0):
            if(threaded):
                f_exit_thread = open(config.exit_thread_file, 'r')

                exit_thread = f_exit_thread.read()

                f_exit_thread.close()

            else:
                exit_thread = 'False'

            initial_time = utime.ticks_ms()
            current_time = utime.ticks_ms()

            while(utime.ticks_diff(current_time, initial_time) < internal_time and exit_thread == 'False'):
                self._leds[internal_led].toggle()

                sleep(0.5)

                current_time = utime.ticks_ms()

                if(threaded):
                    f_exit_thread = open(config.exit_thread_file, 'r')

                    exit_thread = f_exit_thread.read()

                    f_exit_thread.close()

            self._leds[internal_led].value(0)


    def leds(self, leds):
        '''!
            _leds variable modifier

            @param leds					: List of three GPIO LEDs pins

            @return						: Succesfully initialized
        '''

        if(len(leds) == 3):
            self._leds = []

            for led in leds:
                self._leds.append(Pin(int(led), Pin.OUT))

        else:
            return False


    def toggle(self, led):
        '''!
            LED toggler

            @param led					: LED from the list to toggle
        '''

        internal_led	= int(led)

        if(self._leds != None and internal_led < 3):
            self._leds[internal_led].toggle()


    def off(self, led):
        '''!
            LED off switcher

            @param led					: LED from the list to switch off
        '''

        internal_led	= int(led)

        if(self._leds != None and internal_led < 3):
            self._leds[internal_led].value(0)


    def on(self, led):
        '''!
            LED on switcher

            @param led					: LED from the list to switch on
        '''

        internal_led	= int(led)

        if(self._leds != None and internal_led < 3):
            self._leds[internal_led].value(1)
