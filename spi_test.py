#!/usr/bin/env python


from rk3288.gpio import Gpio
from rk3288.spi import Spi

import time
import pdb

BM_FIREFLY=(
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x80,0xC0,0x40,
0xC0,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x80,0x80,
0xB8,0xB8,0xBF,0xFF,0xFF,0xFF,0x7B,0xEA,0xFF,0x3B,0x1B,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x80,0x80,0xC0,0x60,0xA0,0xA0,0xF0,
0xD0,0x78,0x68,0x28,0x2C,0x3C,0x9F,0x01,0x00,0x00,0x00,0x00,0xFD,0x7D,0xC3,0x03,
0x03,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xE0,0xFC,
0x0E,0x03,0x00,0x0C,0x3E,0x3F,0x31,0x30,0x30,0xF8,0xF8,0x3C,0x0E,0x07,0x81,0xC0,
0x7F,0xE0,0x80,0x00,0x03,0x0E,0xFB,0x0E,0xFC,0xC0,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x07,0x3F,0xF8,0xE0,0x80,0x80,0x00,0x0C,0x04,0x04,
0x00,0xC3,0xE7,0x26,0x06,0x06,0x03,0x30,0xF0,0x00,0x03,0x02,0x02,0x03,0xC3,0xE0,
0x3F,0x0F,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x01,0x03,0x03,0x06,0x0E,0x0C,0x0C,0x08,0x18,0x18,0x18,0x18,0x18,0x18,0x18,
0x08,0x08,0x0C,0x06,0x06,0x03,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
)

F8X16={
' ':(0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00),
'!':(0x00,0x00,0x00,0xF8,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x33,0x30,0x00,0x00,0x00),
'"':(0x00,0x10,0x0C,0x06,0x10,0x0C,0x06,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00),
'#':(0x40,0xC0,0x78,0x40,0xC0,0x78,0x40,0x00,0x04,0x3F,0x04,0x04,0x3F,0x04,0x04,0x00),
'$':(0x00,0x70,0x88,0xFC,0x08,0x30,0x00,0x00,0x00,0x18,0x20,0xFF,0x21,0x1E,0x00,0x00),
'%':(0xF0,0x08,0xF0,0x00,0xE0,0x18,0x00,0x00,0x00,0x21,0x1C,0x03,0x1E,0x21,0x1E,0x00),
'&':(0x00,0xF0,0x08,0x88,0x70,0x00,0x00,0x00,0x1E,0x21,0x23,0x24,0x19,0x27,0x21,0x10),
'\'':(0x10,0x16,0x0E,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00),
'(':(0x00,0x00,0x00,0xE0,0x18,0x04,0x02,0x00,0x00,0x00,0x00,0x07,0x18,0x20,0x40,0x00),
')':(0x00,0x02,0x04,0x18,0xE0,0x00,0x00,0x00,0x00,0x40,0x20,0x18,0x07,0x00,0x00,0x00),
'*':(0x40,0x40,0x80,0xF0,0x80,0x40,0x40,0x00,0x02,0x02,0x01,0x0F,0x01,0x02,0x02,0x00),
'+':(0x00,0x00,0x00,0xF0,0x00,0x00,0x00,0x00,0x01,0x01,0x01,0x1F,0x01,0x01,0x01,0x00),
',':(0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x80,0xB0,0x70,0x00,0x00,0x00,0x00,0x00),
'-':(0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01,0x01,0x01,0x01,0x01,0x01),
'.':(0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x30,0x30,0x00,0x00,0x00,0x00,0x00),
'/':(0x00,0x00,0x00,0x00,0x80,0x60,0x18,0x04,0x00,0x60,0x18,0x06,0x01,0x00,0x00,0x00),
'0':(0x00,0xE0,0x10,0x08,0x08,0x10,0xE0,0x00,0x00,0x0F,0x10,0x20,0x20,0x10,0x0F,0x00),
'1':(0x00,0x10,0x10,0xF8,0x00,0x00,0x00,0x00,0x00,0x20,0x20,0x3F,0x20,0x20,0x00,0x00),
'2':(0x00,0x70,0x08,0x08,0x08,0x88,0x70,0x00,0x00,0x30,0x28,0x24,0x22,0x21,0x30,0x00),
'3':(0x00,0x30,0x08,0x88,0x88,0x48,0x30,0x00,0x00,0x18,0x20,0x20,0x20,0x11,0x0E,0x00),
'4':(0x00,0x00,0xC0,0x20,0x10,0xF8,0x00,0x00,0x00,0x07,0x04,0x24,0x24,0x3F,0x24,0x00),
'5':(0x00,0xF8,0x08,0x88,0x88,0x08,0x08,0x00,0x00,0x19,0x21,0x20,0x20,0x11,0x0E,0x00),
'6':(0x00,0xE0,0x10,0x88,0x88,0x18,0x00,0x00,0x00,0x0F,0x11,0x20,0x20,0x11,0x0E,0x00),
'7':(0x00,0x38,0x08,0x08,0xC8,0x38,0x08,0x00,0x00,0x00,0x00,0x3F,0x00,0x00,0x00,0x00),
'8':(0x00,0x70,0x88,0x08,0x08,0x88,0x70,0x00,0x00,0x1C,0x22,0x21,0x21,0x22,0x1C,0x00),
'9':(0x00,0xE0,0x10,0x08,0x08,0x10,0xE0,0x00,0x00,0x00,0x31,0x22,0x22,0x11,0x0F,0x00),
':':(0x00,0x00,0x00,0xC0,0xC0,0x00,0x00,0x00,0x00,0x00,0x00,0x30,0x30,0x00,0x00,0x00),
';':(0x00,0x00,0x00,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x80,0x60,0x00,0x00,0x00,0x00),
'<':(0x00,0x00,0x80,0x40,0x20,0x10,0x08,0x00,0x00,0x01,0x02,0x04,0x08,0x10,0x20,0x00),
'=':(0x40,0x40,0x40,0x40,0x40,0x40,0x40,0x00,0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x00),
'>':(0x00,0x08,0x10,0x20,0x40,0x80,0x00,0x00,0x00,0x20,0x10,0x08,0x04,0x02,0x01,0x00),
'?':(0x00,0x70,0x48,0x08,0x08,0x08,0xF0,0x00,0x00,0x00,0x00,0x30,0x36,0x01,0x00,0x00),
'@':(0xC0,0x30,0xC8,0x28,0xE8,0x10,0xE0,0x00,0x07,0x18,0x27,0x24,0x23,0x14,0x0B,0x00),
'A':(0x00,0x00,0xC0,0x38,0xE0,0x00,0x00,0x00,0x20,0x3C,0x23,0x02,0x02,0x27,0x38,0x20),
'B':(0x08,0xF8,0x88,0x88,0x88,0x70,0x00,0x00,0x20,0x3F,0x20,0x20,0x20,0x11,0x0E,0x00),
'C':(0xC0,0x30,0x08,0x08,0x08,0x08,0x38,0x00,0x07,0x18,0x20,0x20,0x20,0x10,0x08,0x00),
'D':(0x08,0xF8,0x08,0x08,0x08,0x10,0xE0,0x00,0x20,0x3F,0x20,0x20,0x20,0x10,0x0F,0x00),
'E':(0x08,0xF8,0x88,0x88,0xE8,0x08,0x10,0x00,0x20,0x3F,0x20,0x20,0x23,0x20,0x18,0x00),
'F':(0x08,0xF8,0x88,0x88,0xE8,0x08,0x10,0x00,0x20,0x3F,0x20,0x00,0x03,0x00,0x00,0x00),
'G':(0xC0,0x30,0x08,0x08,0x08,0x38,0x00,0x00,0x07,0x18,0x20,0x20,0x22,0x1E,0x02,0x00),
'H':(0x08,0xF8,0x08,0x00,0x00,0x08,0xF8,0x08,0x20,0x3F,0x21,0x01,0x01,0x21,0x3F,0x20),
'I':(0x00,0x08,0x08,0xF8,0x08,0x08,0x00,0x00,0x00,0x20,0x20,0x3F,0x20,0x20,0x00,0x00),
'J':(0x00,0x00,0x08,0x08,0xF8,0x08,0x08,0x00,0xC0,0x80,0x80,0x80,0x7F,0x00,0x00,0x00),
'K':(0x08,0xF8,0x88,0xC0,0x28,0x18,0x08,0x00,0x20,0x3F,0x20,0x01,0x26,0x38,0x20,0x00),
'L':(0x08,0xF8,0x08,0x00,0x00,0x00,0x00,0x00,0x20,0x3F,0x20,0x20,0x20,0x20,0x30,0x00),
'M':(0x08,0xF8,0xF8,0x00,0xF8,0xF8,0x08,0x00,0x20,0x3F,0x00,0x3F,0x00,0x3F,0x20,0x00),
'N':(0x08,0xF8,0x30,0xC0,0x00,0x08,0xF8,0x08,0x20,0x3F,0x20,0x00,0x07,0x18,0x3F,0x00),
'O':(0xE0,0x10,0x08,0x08,0x08,0x10,0xE0,0x00,0x0F,0x10,0x20,0x20,0x20,0x10,0x0F,0x00),
'P':(0x08,0xF8,0x08,0x08,0x08,0x08,0xF0,0x00,0x20,0x3F,0x21,0x01,0x01,0x01,0x00,0x00),
'Q':(0xE0,0x10,0x08,0x08,0x08,0x10,0xE0,0x00,0x0F,0x18,0x24,0x24,0x38,0x50,0x4F,0x00),
'R':(0x08,0xF8,0x88,0x88,0x88,0x88,0x70,0x00,0x20,0x3F,0x20,0x00,0x03,0x0C,0x30,0x20),
'S':(0x00,0x70,0x88,0x08,0x08,0x08,0x38,0x00,0x00,0x38,0x20,0x21,0x21,0x22,0x1C,0x00),
'T':(0x18,0x08,0x08,0xF8,0x08,0x08,0x18,0x00,0x00,0x00,0x20,0x3F,0x20,0x00,0x00,0x00),
'U':(0x08,0xF8,0x08,0x00,0x00,0x08,0xF8,0x08,0x00,0x1F,0x20,0x20,0x20,0x20,0x1F,0x00),
'V':(0x08,0x78,0x88,0x00,0x00,0xC8,0x38,0x08,0x00,0x00,0x07,0x38,0x0E,0x01,0x00,0x00),
'W':(0xF8,0x08,0x00,0xF8,0x00,0x08,0xF8,0x00,0x03,0x3C,0x07,0x00,0x07,0x3C,0x03,0x00),
'X':(0x08,0x18,0x68,0x80,0x80,0x68,0x18,0x08,0x20,0x30,0x2C,0x03,0x03,0x2C,0x30,0x20),
'Y':(0x08,0x38,0xC8,0x00,0xC8,0x38,0x08,0x00,0x00,0x00,0x20,0x3F,0x20,0x00,0x00,0x00),
'Z':(0x10,0x08,0x08,0x08,0xC8,0x38,0x08,0x00,0x20,0x38,0x26,0x21,0x20,0x20,0x18,0x00),
'[':(0x00,0x00,0x00,0xFE,0x02,0x02,0x02,0x00,0x00,0x00,0x00,0x7F,0x40,0x40,0x40,0x00),
'\\':(0x00,0x0C,0x30,0xC0,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x06,0x38,0xC0,0x00),
']':(0x00,0x02,0x02,0x02,0xFE,0x00,0x00,0x00,0x00,0x40,0x40,0x40,0x7F,0x00,0x00,0x00),
'^':(0x00,0x00,0x04,0x02,0x02,0x02,0x04,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00),
'_':(0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x80),
'`':(0x00,0x02,0x02,0x04,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00),
'a':(0x00,0x00,0x80,0x80,0x80,0x80,0x00,0x00,0x00,0x19,0x24,0x22,0x22,0x22,0x3F,0x20),
'b':(0x08,0xF8,0x00,0x80,0x80,0x00,0x00,0x00,0x00,0x3F,0x11,0x20,0x20,0x11,0x0E,0x00),
'c':(0x00,0x00,0x00,0x80,0x80,0x80,0x00,0x00,0x00,0x0E,0x11,0x20,0x20,0x20,0x11,0x00),
'd':(0x00,0x00,0x00,0x80,0x80,0x88,0xF8,0x00,0x00,0x0E,0x11,0x20,0x20,0x10,0x3F,0x20),
'e':(0x00,0x00,0x80,0x80,0x80,0x80,0x00,0x00,0x00,0x1F,0x22,0x22,0x22,0x22,0x13,0x00),
'f':(0x00,0x80,0x80,0xF0,0x88,0x88,0x88,0x18,0x00,0x20,0x20,0x3F,0x20,0x20,0x00,0x00),
'g':(0x00,0x00,0x80,0x80,0x80,0x80,0x80,0x00,0x00,0x6B,0x94,0x94,0x94,0x93,0x60,0x00),
'h':(0x08,0xF8,0x00,0x80,0x80,0x80,0x00,0x00,0x20,0x3F,0x21,0x00,0x00,0x20,0x3F,0x20),
'i':(0x00,0x80,0x98,0x98,0x00,0x00,0x00,0x00,0x00,0x20,0x20,0x3F,0x20,0x20,0x00,0x00),
'j':(0x00,0x00,0x00,0x80,0x98,0x98,0x00,0x00,0x00,0xC0,0x80,0x80,0x80,0x7F,0x00,0x00),
'k':(0x08,0xF8,0x00,0x00,0x80,0x80,0x80,0x00,0x20,0x3F,0x24,0x02,0x2D,0x30,0x20,0x00),
'l':(0x00,0x08,0x08,0xF8,0x00,0x00,0x00,0x00,0x00,0x20,0x20,0x3F,0x20,0x20,0x00,0x00),
'm':(0x80,0x80,0x80,0x80,0x80,0x80,0x80,0x00,0x20,0x3F,0x20,0x00,0x3F,0x20,0x00,0x3F),
'n':(0x80,0x80,0x00,0x80,0x80,0x80,0x00,0x00,0x20,0x3F,0x21,0x00,0x00,0x20,0x3F,0x20),
'o':(0x00,0x00,0x80,0x80,0x80,0x80,0x00,0x00,0x00,0x1F,0x20,0x20,0x20,0x20,0x1F,0x00),
'p':(0x80,0x80,0x00,0x80,0x80,0x00,0x00,0x00,0x80,0xFF,0xA1,0x20,0x20,0x11,0x0E,0x00),
'q':(0x00,0x00,0x00,0x80,0x80,0x80,0x80,0x00,0x00,0x0E,0x11,0x20,0x20,0xA0,0xFF,0x80),
'r':(0x80,0x80,0x80,0x00,0x80,0x80,0x80,0x00,0x20,0x20,0x3F,0x21,0x20,0x00,0x01,0x00),
's':(0x00,0x00,0x80,0x80,0x80,0x80,0x80,0x00,0x00,0x33,0x24,0x24,0x24,0x24,0x19,0x00),
't':(0x00,0x80,0x80,0xE0,0x80,0x80,0x00,0x00,0x00,0x00,0x00,0x1F,0x20,0x20,0x00,0x00),
'u':(0x80,0x80,0x00,0x00,0x00,0x80,0x80,0x00,0x00,0x1F,0x20,0x20,0x20,0x10,0x3F,0x20),
'v':(0x80,0x80,0x80,0x00,0x00,0x80,0x80,0x80,0x00,0x01,0x0E,0x30,0x08,0x06,0x01,0x00),
'w':(0x80,0x80,0x00,0x80,0x00,0x80,0x80,0x80,0x0F,0x30,0x0C,0x03,0x0C,0x30,0x0F,0x00),
'x':(0x00,0x80,0x80,0x00,0x80,0x80,0x80,0x00,0x00,0x20,0x31,0x2E,0x0E,0x31,0x20,0x00),
'y':(0x80,0x80,0x80,0x00,0x00,0x80,0x80,0x80,0x80,0x81,0x8E,0x70,0x18,0x06,0x01,0x00),
'z':(0x00,0x80,0x80,0x80,0x80,0x80,0x80,0x00,0x00,0x21,0x30,0x2C,0x22,0x21,0x30,0x00),
'{':(0x00,0x00,0x00,0x00,0x80,0x7C,0x02,0x02,0x00,0x00,0x00,0x00,0x00,0x3F,0x40,0x40),
'|':(0x00,0x00,0x00,0x00,0xFF,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0x00,0x00,0x00),
'}':(0x00,0x02,0x02,0x7C,0x80,0x00,0x00,0x00,0x00,0x40,0x40,0x3F,0x00,0x00,0x00,0x00),
'~':(0x00,0x06,0x01,0x01,0x02,0x02,0x04,0x04,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00),
}


class Oled:
    WIDTH = 128
    HEIGHT = 64
    WR_CMD  =0
    WR_DATA =1

    def __init__(self, dev, pin_rst, pin_dc):
        self._spi = Spi(dev)

        self._spi.mode = Spi.MODE_3
        self._spi.bits_per_word = 8
        self._spi.speed = 1000*1000
        #spi driver have not supported lsb yet
        #self._spi.lsb_first = True

        Gpio.init()
        self._rst=Gpio(pin_rst)
        self._rst.set_dir(Gpio.OUTPUT)
        self._rst.set_level(Gpio.LOW)

        self._dc=Gpio(pin_dc)
        self._dc.set_dir(Gpio.OUTPUT)
        self._dc.set_level(Gpio.LOW)

        self._rst.set_level(Gpio.HIGH)
        time.sleep(0.001)
        self._rst.set_level(Gpio.LOW)
        time.sleep(0.01)
        self._rst.set_level(Gpio.HIGH)


        self._write(0xAE,Oled.WR_CMD)     #--turn off oled panel
        self._write(0x00,Oled.WR_CMD)     #---set low column address
        self._write(0x10,Oled.WR_CMD)     #---set high column address
        self._write(0x40,Oled.WR_CMD)     #--set start line address  Set omapping RAM Display Start Line (0x00~0x3F)
        self._write(0x81,Oled.WR_CMD)     #--set contrast control register
        self._write(0xCF,Oled.WR_CMD)     # Set SEG Output Current Brightness
        self._write(0xA1,Oled.WR_CMD)     #--Set SEG/Column omapping
        #self._write(0,Oled.WR_DATA)

        self._write(0xC8,Oled.WR_CMD)     #Set COM/Row Scan Direction
        self._write(0xA6,Oled.WR_CMD)     #--set normal display
        self._write(0xA8,Oled.WR_CMD)     #--set multiplex ratio(1 to 64)
        self._write(0x3f,Oled.WR_CMD)     #--1/64 duty
        self._write(0xD3,Oled.WR_CMD)     #-set display offset    Shift omapping RAM Counter (0x00~0x3F)
        self._write(0x00,Oled.WR_CMD)     #-not offset
        self._write(0xd5,Oled.WR_CMD)     #--set display clock divide ratio/oscillator frequency
        self._write(0x80,Oled.WR_CMD)     #--set divide ratio, Set Clock as 100 Frames/Sec
        self._write(0xD9,Oled.WR_CMD)     #--set pre-charge period
        self._write(0xF1,Oled.WR_CMD)     #Set Pre-Charge as 15 Clocks & Discharge as 1 Clock
        self._write(0xDA,Oled.WR_CMD)     #--set com pins hardware configuration
        self._write(0x12,Oled.WR_CMD)     #
        self._write(0xDB,Oled.WR_CMD)     #--set vcomh
        self._write(0x40,Oled.WR_CMD)     #Set VCOM Deselect Level
        self._write(0x20,Oled.WR_CMD)     #-Set Page Addressing Mode (0x00/0x01/0x02)
        self._write(0x02,Oled.WR_CMD)     #
        self._write(0x8D,Oled.WR_CMD)     #--set Charge Pump enable/disable
        self._write(0x14,Oled.WR_CMD)     #--set(0x10) disable
        self._write(0xA4,Oled.WR_CMD)     # Disable Entire Display On (0xa4/0xa5)
        self._write(0xA6,Oled.WR_CMD)     # Disable Inverse Display On (0xa6/a7) 
        self._write(0xAF,Oled.WR_CMD)     #--turn on oled panel
        self._write(0xAF,Oled.WR_CMD)     #display ON

        self.F128X64 = [None]*129 
        for i in range(len(self.F128X64)):  
            self.F128X64[i] = [0]*8  

        self.clear()
        self._set_pos(0,0)


    def _write(self, data, dc):
        if Oled.WR_DATA == dc:
            self._dc.set_level(Gpio.HIGH)
        else:
            self._dc.set_level(Gpio.LOW)

        tbuf = data
        tbuf = ( tbuf & 0x55 ) << 1 | ( tbuf & 0xAA ) >> 1
        tbuf = ( tbuf & 0x33 ) << 2 | ( tbuf & 0xCC ) >> 2
        tbuf = ( tbuf & 0x0F ) << 4 | ( tbuf & 0xF0 ) >> 4
        #reversal buf
        tbuf=int(bin(tbuf)[2:].zfill(8)[::-1], 2)

        self._spi.write([tbuf])
   
    def clear(self):
        for i in range(8):
            self._write(0xb0+i,Oled.WR_CMD)    #set page address (0~7)
            self._write(0x00,Oled.WR_CMD)      #set row low address
            self._write(0x10,Oled.WR_CMD)      #set row high address
            for j in range(128):
                self._write(0,Oled.WR_DATA) 
        self._clear_omap()

    def _clear_omap(self):
        for i in range(len(self.F128X64)):  
            self.F128X64[i] = [0]*8  
   

    def _set_pos(self, x, y):
        self._write(0xb0+y,Oled.WR_CMD)
        self._write(((x&0xf0)>>4)|0x10,Oled.WR_CMD)
        self._write((x&0x0f)|0x01,Oled.WR_CMD) 


    def _the_pow(self, x, y):
        x=1
        if y == 0:
            return 1
        else:
            for j in range(y):
                x=2*x
        return x

    def clear_point(self, x, y):
        if x<=0 or x>128:
            print("clear_point: x:%d is over\n" % x)
            return -1
        if y<=0 or y>64:
            print("clear_point: y:%d is over\n" % y)
            return -1

        if x==1:
            x=128
        else:
            x=x-1

        x=x-1
        y=y-1
        k = y%8
        y=y//8
        omap = self.F128X64[x][y]
        k=self._the_pow(2,k)
        date=(~k)&omap
        self._set_pos(x,y)
        if x%2 == 0:
            self._set_pos(x,y)
            self._write(date,Oled.WR_DATA)
        else:
            self._set_pos(x-1,y)
            self._write(self.F128X64[x-1][y],Oled.WR_DATA)
            self._write(date,Oled.WR_DATA)
        self.F128X64[x][y] = date
        return 0

    def draw_point(self, x, y):
        if x<=0 or x>128:
            print("draw_point: x:%d is over" % x)
            return -1
        if y<=0 or y>64:
            print("draw_point: y:%d is over" % y)
            return -1
        self.clear_point(x,y)

        if x==1:
            x=128
        else:
            x=x-1

        x=x-1
        y=y-1
            
        k = y%8
        y=y//8
        omap = self.F128X64[x][y]
        k=self._the_pow(2,k)
        date=k|omap
        if x%2 == 0:
            self._set_pos(x,y)
            self._write(date,Oled.WR_DATA)
        else:
            self._set_pos(x-1,y)
            self._write(self.F128X64[x-1][y],Oled.WR_DATA)
            self._write(date,Oled.WR_DATA)
        self.F128X64[x][y] = date
        return 0

    def draw_line(self, x0, y0, x1, y1):
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = x1 - x0
        dy = abs(y1 - y0)

        err = dx // 2

        if y0 < y1:
            ystep = 1
        else:
            ystep = -1

        for i in range(x0, x1):
            if steep:
                self.draw_point(y0, i)
            else:
                self.draw_point(i, y0)
            err -= dy
            if err < 0:
                y0 += ystep
                err += dx

    def draw_bitmap(self, bitmap, x, y, w, h):
      for j in range(h): 
          for i in range(w): 
              if (bitmap[i + (j//8)*w] & (1<<(j%8))):
                  self.draw_point(x+i, y+j);

    def draw_char(self, x, y, ch):
        if y<1 or y>4:
            print("draw_char: y:%d is over\n" % y)
            return -1
        if x<1 or x>16:
            print("draw_char: x:%d is over" % x)
            return -1 

        x=(x-1)*8+1
        y=(y-1)*16+1
   
        for i in range(8):
            for j in range(8):
                if (F8X16[ch][i]>>j)&1:
                    self.draw_point(x+i,y+j)
                else:
                    self.clear_point(x+i,y+j)
                if (F8X16[ch][i+8]>>j)&1:
                    self.draw_point(x+i,y+j+8)
                else:   
                    self.clear_point(x+i,y+j+8)
        return 0

    def draw_str(self, x, y, s):
        for c in s:
            self.draw_char(x, y, c)
            x += 1

if __name__ ==  '__main__':
    oled = Oled("/dev/spidev0.0", 'GPIO0A7', 'GPIO7B1')

    oled.draw_str(2,1, 'Hello,Firefly!')
    oled.draw_bitmap(BM_FIREFLY, 44,16, 40, 48)
    oled.draw_line(1,1,128,1)
    oled.draw_line(1,1,1,64)
    oled.draw_line(128,1,128,64)
    oled.draw_line(1,64,128,64)
