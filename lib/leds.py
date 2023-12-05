#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''!
    leds

    @file       : leds.py
    @brief      : LEDs manager module

    @author     : Veltys
    @date       : 2023-12-05
    @version    : 1.1.0
    @usage      : (imported when needed)
    @note       : ...
'''


from machine import Pin                                                         # GPIO pins management


class leds:
    _leds = None


    def __init__(self, leds = None):
        '''!
            Class constructor

            Initializes default values of the class

            @param leds					: List of three GPIO LEDs pins
        '''

        if(leds is not None):
            self.leds(leds)


    def leds(self, leds):
        '''!
            _leds variable modifier

            @param leds					: List of GPIO LEDs pins

            @return						: Succesfully initialized
        '''

        if(leds is not None):
            self._leds = []

            for led in leds:
                self._leds.append(Pin(led, Pin.OUT))

            return True

        else:
            return False


    def toggle(self, led = None):
        '''!
            LED toggler

            @param led					: LED from the list to toggle
        '''

        if(self._leds is not None):
            self._leds[int(led)].toggle()

        else:
            for i, _ in enumerate(self._leds):
                self.toggle(i)


    def off(self, led = None):
        '''!
            LED off switcher

            @param led					: LED from the list to switch off
        '''

        if(self._leds is not None):
            self._leds[int(led)].value(0)

        else:
            for i, _ in enumerate(self._leds):
                self.off(i)


    def on(self, led = None):
        '''!
            LED on switcher

            @param led					: LED from the list to switch on
        '''

        if(self._leds is not None):
            self._leds[int(led)].value(1)

        else:
            for i, _ in enumerate(self._leds):
                self.on(i)
