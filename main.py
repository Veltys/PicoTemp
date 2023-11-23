#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''!
    main

    @file       : main.py
    @brief      : Main module

    @author     : Veltys
    @date       : 2023-11-25
    @version    : 2.3.0
    @usage      : python3 main.py | ./main.py
    @note       : ...
'''


import _thread                                                                  # Low-level threads management
import errno                                                                    # Error codes
import sys                                                                      # System-specific parameters and functions
import time                                                                     # Time manipulation

from OLED_1inch3 import OLED_1inch3                                             # OLED screen hardware management
from dht11 import dht11                                                         # DHT11 sensor management
from machine import Pin                                                         # GPIO pins management
from server import server                                                       # HTTP server
from wifi import wifi                                                           # WiFi hardware management
import network                                                                  # Network management
import ntptime


try:
    from config import config                                                   # Configuration

except ImportError:
    print('Error: Config file not found', file = sys.stderr)
    sys.exit(errno.ENOENT)


DEBUG = False
WIFI_STAT = {
    network.STAT_IDLE: 'IDLE',
    network.STAT_CONNECTING: 'CONNECTING',
    network.STAT_WRONG_PASSWORD: 'WRONG_PASSWORD',
    network.STAT_NO_AP_FOUND: 'NO_AP_FOUND',
    network.STAT_CONNECT_FAIL: 'CONNECT_FAIL',
    network.STAT_GOT_IP: 'SUCCESS'
}


bound = None
do_exit = [ False, False ]
ip = '0.0.0.0'
measures = []
uptime_initial = None

for i, _ in enumerate(config.dht11_pins):
    measures.append({
        'humidity': None,
        'temperature': None,
    })


def global_exit():
    global do_exit

    if (DEBUG):
        print(
            f'''

Status:

    {{ do_exit[0] ➡ { do_exit[0] } }},

    {{ do_exit[1] ➡ { do_exit[1] } }},

''')
    do_exit[0] = True
    do_exit[1] = True


def button_event(buttons, oled, screen_on):
    if(not buttons[0].value()):
        screen_on = not screen_on

        time.sleep(0.5)

        if(screen_on):
            if (DEBUG):
                print('Switching screen on 💡')

            oled.write_cmd(0xAD)
            oled.write_cmd(0x8A)
            oled.write_cmd(0XAF)

        else:
            if (DEBUG):
                print('Switching screen off 🕯️')

            oled.fill(0xFFFF)
            oled.write_cmd(0xAE)

    elif (not (buttons[1].value())):
        if (DEBUG):
            print('Bye, bye 👋🏼')

        global_exit()

    return screen_on


def paint_screen(oled, wifi_image, server_image, temperature, humidity, ip, now, uptime):
    OFFSET_H = 1
    OFFSET_V = 0

    oled.fill(0) # Clean screen

    oled.blit(wifi_image, 0, 0 + OFFSET_V)

    if (bound is not None):
        oled.blit(server_image, 34 + OFFSET_H, 0 + OFFSET_V)

    oled.text(temperature, 68 + OFFSET_H * 2 + 2, 0 + OFFSET_V + 6, oled.white)

    oled.text(humidity, 68 + OFFSET_H * 2 + 2, 10 + OFFSET_V + 6, oled.white)

    oled.rect(0, 32 + OFFSET_V, 128, 2, oled.white, True)

    oled.text(ip, int((128 - len(ip) * 8) / 2), 36 + OFFSET_V, oled.white)

    oled.text(now, int((128 - len(now) * 8) / 2), 46 + OFFSET_V, oled.white)

    if (uptime_initial is not None):
        oled.text(uptime, int((128 - len(uptime) * 8) / 2), 56 + OFFSET_V, oled.white)

    oled.show()


def screen_buttons_manager():
    NUM_SERVER_IMAGES = 2
    NUM_WIFI_IMAGES = 4


#   global bound
#   global do_exit
#   global ip
#   global measures
#   global uptime_initial

    buttons = [
        Pin(config.buttons_pins[0], Pin.IN, Pin.PULL_UP),
        Pin(config.buttons_pins[1], Pin.IN, Pin.PULL_UP),
    ]
    humidity = None
    image_error = OLED_1inch3.load_pbm('./resources/error.pbm', 32, 30)
    now = None
    now_text = ''
    num_measures = len(measures)
    oled = OLED_1inch3()
    screen_on = True
    server_images = []
    server_image_number = 0
    temperature = None
    ticks = 60 * 5
    uptime = ''
    wifi_images = []
    wifi_image_number = 0

    for i in range(1, NUM_WIFI_IMAGES + 1):
        wifi_images.append(OLED_1inch3.load_pbm(f"./resources/wifi{ i }.pbm", 32, 30))

    for i in range(1, NUM_SERVER_IMAGES + 1):
        server_images.append(OLED_1inch3.load_pbm(f"./resources/server{ i }.pbm", 32, 30))


    while(not do_exit[1]):
        for i in range(ticks):
            if(DEBUG):
                print(f"i = { i }")

            if(do_exit[1]):
                if(DEBUG):
                    print('Exit event detected 👋🏼')

                global_exit()

            if(not(buttons[0].value()) or not(buttons[1].value())):
                if(DEBUG):
                    print('Button event detected 😮')
                    print(
f'''
Status:
    {{ buttons[0].value() ➡ { buttons[0].value() } (screen on / off) }},
    {{ buttons[1].value() ➡ { buttons[1].value() } (exit) }},
'''
                    )

                screen_on = button_event(buttons, oled, screen_on)

                break

            if(screen_on):
                if(ip == '0.0.0.0'):
                    wifi_image_number = i % NUM_WIFI_IMAGES

                elif(ip == 'WiFi Error'):
                    wifi_image_number = -1

                else:
                    wifi_image_number = NUM_WIFI_IMAGES - 1

                if(bound is not None):
                    if(bound):
                        server_image_number = i % NUM_SERVER_IMAGES

                    else:
                        server_image_number = -1

                measures_index = i // (ticks // num_measures)

                if(measures[measures_index]['temperature'] is not None):
                    temperature = f"T: { measures[measures_index]['temperature'] } C"

                else:
                    temperature = "T: ?? C"

                if(measures[measures_index]['humidity'] is not None):
                    humidity = f"H: { measures[measures_index]['humidity'] } %"

                else:
                    humidity = "H: ?? %"

                if(i % 100 == 0):
                    now = time.localtime(time.time() + 60 * 60)                 # TODO: DST handling

                if(i % 6 == 0 or (i - 1) % 6 == 0 or (i - 2) % 6 == 0):
                    now_text = f"{ '{:0>2}'.format(now[3]) }:{ '{:0>2}'.format(now[4]) } { '{:0>2}'.format(now[2]) }/{ '{:0>2}'.format(now[1]) }/{ now[0] }"

                else:
                    now_text = f"{ '{:0>2}'.format(now[3]) } { '{:0>2}'.format(now[4]) } { '{:0>2}'.format(now[2]) }/{ '{:0>2}'.format(now[1]) }/{ now[0] }"

                if(uptime_initial is not None):
                    if(i % 2 == 0):
                        uptime_diff = time.time() - uptime_initial

                        (minutes, seconds) = divmod(uptime_diff, 60)
                        (hours, minutes) = divmod(minutes, 60)
                        (days, hours) = divmod(hours, 24)

                        uptime = f"Up: { days } d { '{:0>2}'.format(hours) }:{ '{:0>2}'.format(minutes) }:{ '{:0>2}'.format(seconds) }"

                paint_screen(
                    oled,
                    wifi_images[wifi_image_number] if(wifi_image_number >= 0) else image_error,
                    server_images[server_image_number] if(server_image_number >= 0) else image_error,
                    temperature,
                    humidity,
                    ip,
                    now_text,
                    uptime
                )

            time.sleep(0.1)

        if(i >= 60 and screen_on):
            if(DEBUG):
                print('Switching screen off 🕯️')

            screen_on = False

            oled.fill(0xFFFF)
            oled.write_cmd(0xAE)

    oled.fill(0xFFFF)
    oled.write_cmd(0xAE)


def main(argv = sys.argv[1:]): # @UnusedVariable
    '''!
        Performs the needed operations to work

        @param argv:    Program arguments

        @return:        Return code
    '''

    global bound
    global do_exit
    global ip
    global measures
    global uptime_initial

    connection = wifi(ssid = config.wifi_ssid, password = config.wifi_password)
    s = server()
    sensors = [dht11(pin) for pin in config.dht11_pins]

    for i, sensor in enumerate(sensors):
        sensor.measure()

        measures[i]['humidity'] = sensor.humidity()
        measures[i]['temperature'] = sensor.temperature()

    # Thread to make screen_buttons_manager
    _thread.start_new_thread(screen_buttons_manager, ())

    time.sleep(1)

    connected = connection.connect()

    if(DEBUG):
        print('WiFi connect...')

    if(connected == network.STAT_GOT_IP):
        ip = connection.ip()

        if(DEBUG):
            print('WiFi connected 😁')
            print(ip)

        ntptime.host = "hora.roa.es"

        try:
            ntptime.settime()

        except OSError:
            pass

        else:
            uptime_initial = time.time()

        bound = s.bind(ip = connection.ip())

        if(bound):
            if(DEBUG):
                print('Server bound 👍🏼')

            while(not do_exit[0]):
                if(measures[0]['humidity'] is not None and measures[0]['temperature'] is not None):
                    if(DEBUG):
                        print(f"Temp: { measures[0]['temperature'] }º C")

                    s.accept([measure.get('temperature') for measure in measures], ip)

                else:
                    if(DEBUG):
                        print('Cannot get temp 😭')

                for i, sensor in enumerate(sensors):
                    sensor.measure()

                    measures[i]['humidity'] = sensor.humidity()
                    measures[i]['temperature'] = sensor.temperature()

                # TODO: check WiFi status

        else:
            if(DEBUG):
                print('Cannot bind 👎🏼')

    else:
        ip = 'WiFi Error'

        if(DEBUG):
            print(f"WiFi error: { WIFI_STAT[connected] }")


    if(not do_exit[0]):
        time.sleep(30)

    global_exit()

    time.sleep(1)

    connection.disconnect()

    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
