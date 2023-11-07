#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''!
    main

    @file		: main.py
    @brief		: Main module

    @author		: Veltys
    @date		: 2023-10-30
    @version	: 1.0.2
    @usage		: python3 main.py | ./main.py
    @note		: ...
'''


from time import sleep															# Sleep function
import _thread																	# Low-level threads management
import errno                                                                    # Error codes
import sys																		# System-specific parameters and functions

from exitstatus import ExitStatus                                               # POSIX exit status codes

from dht11 import dht11															# DHT11 sensor management
from leds import leds															# LEDs management
from server import server														# HTTP server
from wifi import wifi															# WiFi hardware management


try:
    from config import config                                                   # Configuration

except ImportError:
    print('Error: Config file not found', file = sys.stderr)
    sys.exit(errno.ENOENT)


DEBUG = False


def main(argv = sys.argv[1:]):													# @UnusedVariable
    '''!
        Performs the needed operations to work

        @param argv:    Program arguments

        @return:        Return code
    '''

    connection = wifi(ssid = config.wifi_ssid, password = config.wifi_password)
    lds = leds(config.leds_pins)
    s = server()
    sensor = dht11(config.dht11_pin)

    f_exit_thread = open(config.exit_thread_file, 'w')
    f_exit_thread.write('False')
    f_exit_thread.close()

    _thread.start_new_thread(lds.blink, (1, sys.maxsize, True))

    sleep(1)

    if(connection.connect()):
        f_exit_thread = open(config.exit_thread_file, 'w')
        f_exit_thread.write('True')
        f_exit_thread.close()

        lds.off(1)
        lds.on(2)

        if(DEBUG):
            print('My IP is: ' + connection.ip())

        if(s.bind(ip = connection.ip())):
            while(True):
                sensor.measure()

                if(sensor.temperature() != None):
                    s.accept(sensor.temperature())

    else:
        f_exit_thread = open(config.exit_thread_file, 'w')
        f_exit_thread.write('True')
        f_exit_thread.close()

        lds.off(1)
        lds.on(0)

    connection.disconnect()

    for i in range(3):
        lds.off(i)

    sys.exit(ExitStatus.success)


if __name__ == "__main__":
    main(sys.argv[1:])
