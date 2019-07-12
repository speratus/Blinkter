import asyncio
import blinkt

##import .board

#from copy import deepcopy

from .led import LED
from .threads import FlashThread

class Pixel:
    def __init__(self, board, addr):
        self.board = board
        self.addr = addr
        self.brightness = 0.1
##        self.r = 0
##        self.g = 0
##        self.b = 0
        self.orgb = [0, 0, 0]
        self.rgb = [0, 0, 0]
        self.increment_amount = 10
        self.bi = 0.1

##    async def blinkt_go(self):
##        blinkt.set_pixel(self.addr, self.rgb[LED.RED], self.rgb[LED.GREEN], self.rgb[LED.BLUE], brightness=self.brightness)
##        #blinkt.set_brightness(self.brightness)
##        blinkt.show()
##        print('called from the second thread and event loop')

    def _keep_color(self):
        self.orgb[LED.RED.value] = self.rgb[LED.RED.value]
        self.orgb[LED.GREEN.value] = self.rgb[LED.GREEN.value]
        self.orgb[LED.BLUE.value] = self.rgb[LED.BLUE.value]

    def _revert_color(self):
        self.rgb[LED.RED.value] = self.orgb[LED.RED.value]
        self.rgb[LED.GREEN.value] = self.orgb[LED.GREEN.value]
        self.rgb[LED.BLUE.value] = self.orgb[LED.BLUE.value]

    def black(self):
        self._keep_color()
        
        self.rgb[LED.RED.value] = 0
        self.rgb[LED.GREEN.value] = 0
        self.rgb[LED.BLUE.value] = 0
##        blinkt.set_pixel(self.addr, self.r, self.g, self.b)
        self.draw()

    def white(self):
        self._keep_color()
        
        self.rgb[LED.RED.value] = 255
        self.rgb[LED.GREEN.value] = 255
        self.rgb[LED.BLUE.value] = 255

    def draw(self):
##        p = deepcopy(self)
##        board.thread.draw_pixel(p)
##        print('drew the pixel. If nothing shows, uncomment lines 45 and 55.')
        blinkt.set_pixel(self.addr, self.rgb[LED.RED.value], self.rgb[LED.GREEN.value], self.rgb[LED.BLUE.value], brightness=self.brightness)
        blinkt.show()
##        print('drew the pixel. If nothing shows, then there is an error somewhere.')
        
        
    def increment(self, led: LED, amount=0):
        self._keep_color()
        
        a = amount if amount is not 0 else self.increment_amount
        print(f'using value {a}')
        c = self.rgb[led.value]
        if c+a > 255:
            c = 255
            self.rgb[led.value] = c
        else:
            c += a
            self.rgb[led.value] = c
##        self.rgb[led] = c
        self.draw()

    def decrement(self, led: LED, amount=0):
        self._keep_color()

        a = amount if amount is not 0 else self.increment_amount
        print(f'using value {a}')
        c = self.rgb[led.value]
        if c+a < 0:
            c = 0
            self.rgb[led.value]
        else:
            c -= a
            self.rgb[led.value] = c
##        self.rgb[led] = c
        self.draw()

    def set_led(self, led: LED, value: int):
        self._keep_color()

        if value > 255:
            self.rgb[led.value] = 255
        elif value < 0:
            self.rgb[led.value] = 0
        else:
            self.rgb[led.value] = value

        self.draw()

    def set_color(self, r: int, g: int, b: int):
        self._keep_color()

        for i in range(3):
            c = 0
            if i == 0:
                c = r
            elif i == 1:
                c = g
            else:
                c = b

            if c > 255:
                self.rgb[i] = 255
            elif c < 0:
                self.rgb[i] = 0
            else:
                self.rgb[i] = c

        self.draw()
                
    def increment_brightness(self, amount=0.0):
        a = amount if amount is not 0.0 else self.bi
        if self.bi+a > 1.0:
            self.bi = 1.0
        elif self.bi < 0.0:
            self.bi = 0
        else:
            self.bi += a

        self.draw()
        
    def red(self):
        self.set_led(LED.RED, 255)
        self.set_led(LED.GREEN, 0)
        self.set_led(LED.BLUE, 0)
        self.draw()
        
    def green(self):
        self.set_led(LED.RED, 0)
        self.set_led(LED.GREEN, 255)
        self.set_led(LED.BLUE, 0)
        self.draw()
        
    def blue(self):
        self.set_led(LED.RED, 0)
        self.set_led(LED.GREEN, 0)
        self.set_led(LED.BLUE, 255)
        
    def flash(self, r=0, g=0, b=0, length=0.25):
        thread = FlashThread(self, length)
        if r == 0 and g == 0 and b == 0:
            self.black()
            self._revert_color()
            self.draw()
            thread.start()
        else:
            self.set_color(r, g, b)
            thread.start()
