#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''!
    main

    @file       : main.py
    @brief      : Main module

    @author     : Veltys
    @date       : 2024-11-07
    @version    : 2.6.1
    @usage      : python3 main.py | ./main.py
    @note       : ...
'''


import _thread                                                                              # Low-level threads management
import errno                                                                                # Error codes
import sys                                                                                  # System-specific parameters and functions
import time                                                                                 # Time manipulation

from OLED_1inch3 import OLED_1inch3                                                         # OLED screen hardware management
from dht11 import dht11                                                                     # DHT11 sensor management
from dht22 import dht22                                                                     # DHT22 sensor management
# from leds import leds                                                                     # LEDs management
from machine import Pin                                                                     # GPIO pins management
from server import server                                                                   # HTTP server
from wifi import wifi                                                                       # WiFi hardware management
import network                                                                              # Network management
import ntptime                                                                              # NTP time management


try:
    from config import config                                                               # Configuration

except ImportError:
    print('Error: Config file not found', file = sys.stderr)
    sys.exit(errno.ENOENT)


DEBUG = False
HOUR_OFFSET = 60 * 60
PBM_HEIGHT = 16
PBM_WIDTH = 16
VERSION = '2.6.1'
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

for i, _ in enumerate(config.dht11_pins + config.dht22_pins):
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


def determine_image_number(i, total_ip, total_server):
    # global bound
    # global ip

    res = []

    if(ip == '0.0.0.0'):
        res.append(i % total_ip)

    elif(ip == 'WiFi Error'):
        res.append(-1)

    else:
        res.append(total_ip - 1)

    if(bound is not None and bound):
        res.append(i % total_server)

    else:
        res.append(-1)

    if(DEBUG):
        print(f"wifi_image_number = { res[0] }, server_image_number = { res[1] }")

    return res[0], res[1]


def determine_uptime():
    # global uptime_initial

    if(uptime_initial is not None):
        uptime_diff = time.time() - uptime_initial

        (minutes, seconds) = divmod(uptime_diff, 60)
        (hours, minutes) = divmod(minutes, 60)
        (days, hours) = divmod(hours, 24)

        uptime = f"Up: { days } d { '{:0>2}'.format(hours) }:{ '{:0>2}'.format(minutes) }:{ '{:0>2}'.format(seconds) }"

    else:
        uptime = None

    return uptime


def get_temperature_humidity():
    # global measures

    num_measures = len(measures)


    def inner_function(i, total_ticks):
        # global measures

        nonlocal num_measures

        max_portion = 10
        max_ticks_per_sensor = total_ticks // max_portion                               # Calculate the maximum number of ticks per sensor, not to exceed a quarter of total_ticks
        switch_rate = min(total_ticks // num_measures, max_ticks_per_sensor)            # Calculate how often to switch sensors, based on the total number of sensors and the max ticks per sensor
        measures_index = (i // switch_rate) % num_measures                              # Calculate the sensor index based on the current tick


        if measures[measures_index]['temperature'] is not None:
            temperature = f"T{ measures_index + 1 }: { '{:0>2}'.format(measures[measures_index]['temperature']) }C"

        else:
            temperature = f"T{ measures_index + 1 }: ??C"

        if measures[measures_index]['humidity'] is not None:
            humidity = f"H{ measures_index + 1 }: {'{:0>2}'.format(measures[measures_index]['humidity']) }%"

        else:
            humidity = f"H{ measures_index + 1 }: ??%"

        return temperature, humidity

    return inner_function


def paint_screen(oled, wifi_image, server_image, thermometer_image, temperature, humidity, ip, now, uptime):
    OFFSET_H = 3
    OFFSET_V = 2
    RECT_HEIGHT = 2
    TEXT_HEIGHT = 8

    position_h = 0
    position_v = 0

    oled.fill(0)                                                                            # Clean screen

    oled.blit(thermometer_image, position_h * (PBM_WIDTH + OFFSET_H), position_v * (PBM_HEIGHT + OFFSET_V))

    position_h += 1

    oled.blit(wifi_image, position_h * (PBM_WIDTH + OFFSET_H), position_v * (PBM_HEIGHT + OFFSET_V))

    position_h += 1

    if(bound is not None):
        oled.blit(server_image, position_h * (PBM_WIDTH + OFFSET_H), position_v * (PBM_HEIGHT + OFFSET_V))

    position_h += 1

    oled.text(temperature, position_h * (PBM_WIDTH + OFFSET_H), position_v * (PBM_HEIGHT + OFFSET_V), oled.white)

    position_v += 1

    oled.text(humidity, position_h * (PBM_WIDTH + OFFSET_H), position_v * (TEXT_HEIGHT + OFFSET_V), oled.white)

    position_v += 1

    oled.rect(0, position_v * (TEXT_HEIGHT + OFFSET_V), 128, RECT_HEIGHT, oled.white, True)

    position_v = 2

    oled.text(ip, int((128 - len(ip) * 8) / 2), position_v * (TEXT_HEIGHT + OFFSET_V) + RECT_HEIGHT + OFFSET_V, oled.white)

    position_v += 1

    oled.text(now, int((128 - len(now) * 8) / 2), position_v * (TEXT_HEIGHT + OFFSET_V) + RECT_HEIGHT + OFFSET_V, oled.white)

    position_v += 1

    if(uptime is not None):
        oled.text(uptime, int((128 - len(uptime) * 8) / 2), position_v * (TEXT_HEIGHT + OFFSET_V) + RECT_HEIGHT + OFFSET_V, oled.white)

    else:
        oled.text('Up: calc...', int((128 - 11 * 8) / 2), position_v * (TEXT_HEIGHT + OFFSET_V) + RECT_HEIGHT + OFFSET_V, oled.white)

    position_v += 1

    oled.text(f"PicoTemp { VERSION } A", int((128 - 16 * 8) / 2), position_v * (TEXT_HEIGHT + OFFSET_V) + RECT_HEIGHT + OFFSET_V, oled.white)

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
    image_error = OLED_1inch3.load_pbm('./resources/error.pbm', PBM_WIDTH, PBM_HEIGHT)
    image_thermometer = OLED_1inch3.load_pbm('./resources/thermometer.pbm', PBM_WIDTH, PBM_HEIGHT)
#   led = leds(config.leds_pins)
    now = None
    now_text = ''
    oled = OLED_1inch3()
    screen_on = True
    server_images = []
    server_image_number = 0
    temperature = None
    total_ticks = 60 * 5
    uptime = ''
    wifi_images = []
    wifi_image_number = 0

    for i in range(1, NUM_WIFI_IMAGES + 1):
        wifi_images.append(OLED_1inch3.load_pbm(f"./resources/wifi{ i }.pbm", PBM_WIDTH, PBM_HEIGHT))

    for i in range(1, NUM_SERVER_IMAGES + 1):
        server_images.append(OLED_1inch3.load_pbm(f"./resources/server{ i }.pbm", PBM_WIDTH, PBM_HEIGHT))


    while(not do_exit[1]):
        for i in range(total_ticks):
            if(DEBUG):
                print(f"i = { i }")

            if(do_exit[1]):
                if(DEBUG):
                    print('Exit event detected 👋🏼')

#               led.off(0)

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
#               led.off(0)

                wifi_image_number, server_image_number = determine_image_number(i, NUM_WIFI_IMAGES, NUM_SERVER_IMAGES)
                wifi_image = wifi_images[wifi_image_number] if(wifi_image_number >= 0) else image_error
                server_image = server_images[server_image_number] if(server_image_number >= 0) else image_error
                thermometer_image = image_thermometer
                get_temp_hum = get_temperature_humidity()
                temperature, humidity = get_temp_hum(i, total_ticks)
                now = time.localtime(time.time() + HOUR_OFFSET + (HOUR_OFFSET if config.dst else 0)) if(i % 100 == 0) else now   # TODO: DST handling still needed
                now_text = f"{ '{:0>2}'.format(now[3]) }:{ '{:0>2}'.format(now[4]) } { '{:0>2}'.format(now[2]) }/{ '{:0>2}'.format(now[1]) }/{ now[0] }" if i % 6 in (0, 1, 2) else f"{ '{:0>2}'.format(now[3]) } { '{:0>2}'.format(now[4]) } { '{:0>2}'.format(now[2]) }/{ '{:0>2}'.format(now[1]) }/{ now[0] }"
                uptime = determine_uptime() if(i % 2 == 0) else uptime

                paint_screen(
                    oled,
                    wifi_image,
                    server_image,
                    thermometer_image,
                    temperature,
                    humidity,
                    ip,
                    now_text,
                    uptime
                )

            else:
#               if(i % 10 == 0):
#                   led.toggle(0)

                pass

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
    sensors += [dht22(pin) for pin in config.dht22_pins]

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
            pass

        finally:
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
