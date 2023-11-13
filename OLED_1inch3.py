#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''!
    OLED_1inch3

    @file       : OLED_1inch3.py
    @brief      : Pico-OLED-1.3 class

    @author     : Waveshare
    @author     : Veltys
    @date       : 2023-11-12
    @version    : 1.1.1
    @usage      : (imported when needed)
    @note       : ...
'''


import time

from machine import Pin, SPI
import framebuf


DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9


class OLED_1inch3(framebuf.FrameBuffer):
    def __init__(self):
        '''!
            Class constructor

            Initializes default values of the class and the display
        '''

        self.width = 128
        self.height = 64

        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)

        self.cs(1)

        self.spi = SPI(1)
        self.spi = SPI(1, 2000_000)
        self.spi = SPI(1, 20000_000, polarity = 0, phase = 0, sck = Pin(SCK), mosi = Pin(MOSI), miso = None)

        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)

        self.buffer = bytearray(self.height * self.width // 8)

        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_HMSB)

        self.init_display()

        self.white = 0xffff
        self.balck = 0x0000


    def init_display(self):
        '''!
            Initialize display

            Initializes the OLED display by sending a sequence of commands
        '''

        self.rst(1)

        time.sleep(0.001)

        self.rst(0)

        time.sleep(0.01)

        self.rst(1)

        self.write_cmd(0xAE)                                                    # Turn off OLED display

        self.write_cmd(0x00)                                                    # Set lower column address
        self.write_cmd(0x10)                                                    # Set higher column address

        self.write_cmd(0xB0)                                                    # Set page address

        self.write_cmd(0xDC)                                                    # Set display start line
        self.write_cmd(0x00)
        self.write_cmd(0x81)                                                    # Contract control
        self.write_cmd(0x6F)                                                    # 128
        self.write_cmd(0x21)                                                    # Set Memory addressing mode (0x20/0x21) #

        self.write_cmd(0xA0)                                                    # Set segment remap
        self.write_cmd(0xC0)                                                    # Com scan direction
        self.write_cmd(0xA4)                                                    # Disable Entire Display On (0xA4/0xA5)

        self.write_cmd(0xA6)                                                    # normal / reverse
        self.write_cmd(0xA8)                                                    # Multiplex ratio
        self.write_cmd(0x3F)                                                    # duty = 1 / 64

        self.write_cmd(0xD3)                                                    # Set display offset
        self.write_cmd(0x60)

        self.write_cmd(0xD5)                                                    # Set osc division
        self.write_cmd(0x41)

        self.write_cmd(0xD9)                                                    # Set pre-charge period
        self.write_cmd(0x22)

        self.write_cmd(0xDB)                                                    # Set vcomh
        self.write_cmd(0x35)

        self.write_cmd(0xAD)                                                    # Set charge pump enable
        self.write_cmd(0x8A)                                                    # Set DC-DC enable (a=0:disable; a=1:enable)
        self.write_cmd(0XAF)


    def show(self):
        '''!
            Show buffer on the display

            Transfers the buffer data to the OLED display for rendering
        '''

        self.write_cmd(0xb0)

        for page in range(0, 64):
            self.column = 63 - page

            self.write_cmd(0x00 + (self.column & 0x0f))
            self.write_cmd(0x10 + (self.column >> 4))

            for num in range(0, 16):
                self.write_data(self.buffer[page * 16 + num])


    @staticmethod
    def load_pbm(filename, width, height):
        '''!
            Load image from PBM file

            Loads an image from a PBM (Portable BitMap) file and returns a FrameBuffer object


            @param  filename    : Path to the PBM file
            @param  width       : Width of the image
            @param  height      : Height of the image

            @return             : FrameBuffer object containing the image data
        '''

        with open(filename, 'rb') as f:
            f.readline()                                                        # Magic number
            f.readline()                                                        # Creator comment
            f.readline()                                                        # Dimensions

            data = bytearray(f.read())

        return framebuf.FrameBuffer(data, width, height, framebuf.MONO_HLSB)


    def write_cmd(self, cmd):
        '''!
            Write command to the OLED display

            Sends a command to the OLED display

            @param  cmd         : Command to be sent
        '''

        self.cs(1)

        self.dc(0)

        self.cs(0)

        self.spi.write(bytearray([cmd]))

        self.cs(1)


    def write_data(self, buf):
        '''!
            Write data to the OLED display

            Sends data to the OLED display

            @param  buf         : Data to be sent
        '''

        self.cs(1)

        self.dc(1)

        self.cs(0)

        self.spi.write(bytearray([buf]))

        self.cs(1)
