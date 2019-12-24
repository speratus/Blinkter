#  MIT License
#
#  Copyright (c) 2019 speratus
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import blinkt


from .led import LED
from .threads import FlashThread, BlinkThread, AdvancedBlinkThread


class Pixel:
    """
    Represents a single pixel on the :class:`BlinktBoard`.
    
    This class is the main point of interaction between the user and the blinkt board. Any operation done on a single pixel
    should be executed from an object of this class.
    
    Usage
    ----------
    Users should not attempt to instantiate this class directly. Instead use the :func:`BlinktBoard.get_pixel` to acquire an instance of 
    this class.
    
    .. code-block:: python3
        from blinkter import BlintkBoard
        
        board = BlinktBoard()
        pixel = board.get_pixel(0)
    """
    def __init__(self, board, addr):
        self.board = board
        self.addr = addr
        self.brightness = 0.1

        self.orgb = [0, 0, 0]
        self.rgb = [0, 0, 0]
        self.increment_amount = 10
        self.bi = 0.1
        self.blinking_thread = None
        self.save_brightness = True
        self.ob = 0.1

    def _keep_brightness(self):
        if self.save_brightness:
            self.ob = self.brightness

    def _revert_brightness(self):
        if self.save_brightness:
            self.brightness = self.ob

    def _keep_color(self):
        self.orgb[LED.RED.value] = self.rgb[LED.RED.value]
        self.orgb[LED.GREEN.value] = self.rgb[LED.GREEN.value]
        self.orgb[LED.BLUE.value] = self.rgb[LED.BLUE.value]

        self._keep_brightness()

    def revert_color(self):
        """
        Resets this pixel's color to the most recently used color.
        """
        r = self.orgb[LED.RED.value]
        g = self.orgb[LED.GREEN.value]
        b = self.orgb[LED.BLUE.value]
        
        self._keep_color()
        self.rgb[LED.RED.value] = r
        self.rgb[LED.GREEN.value] = g
        self.rgb[LED.BLUE.value] = b

        self._revert_brightness()
        
        self.draw()

    def black(self):
        """
        Turns this pixel off completely.
        """
        self._keep_color()
        
        self.rgb[LED.RED.value] = 0
        self.rgb[LED.GREEN.value] = 0
        self.rgb[LED.BLUE.value] = 0

        self.draw()

    def white(self):
        """
        Sets all three primary LEDs in this pixel to maximum levels to make this pixel appear white.
        """
        self._keep_color()
        
        self.rgb[LED.RED.value] = 255
        self.rgb[LED.GREEN.value] = 255
        self.rgb[LED.BLUE.value] = 255
        
        self.draw()

    def draw(self):
        """
        Sends this pixel's internal state out to the GPIO, causing the pixel to light up.
        
        Under normal circumstances, users should not have to call this method.
        """

        self.board.lock.acquire(blocking=True, timeout=1)
        blinkt.set_pixel(self.addr, self.rgb[LED.RED.value], self.rgb[LED.GREEN.value], self.rgb[LED.BLUE.value], brightness=self.brightness)
        blinkt.show()
        self.board.lock.release()

    def increment(self, led: LED, amount=0, wrap_around=False):
        """
        Increments the selected LED's brightness by the specified amount.
        
        Parameters
        ------------------
        :param led: :class:`LED`
            specifies which LED's brightness should be incremented.
        
        :param amount: Optional[int]
            The amount to increase the brightness of the specified LED.

        :param wrap_around: Optional[boolean]
            Determines whether the pixel will set the color brightness to zero for any value that exceeds 255.
            The default is ``False``. By default, :meth:`increment` prevents color brightness from being invalid by
            setting the maximum at 255.
        """
        self._keep_color()
        too_hi = 0 if wrap_around is True else 255
        too_lo = 255 if wrap_around is True else 0
        
        a = amount if amount is not 0 else self.increment_amount

        c = self.rgb[led.value]
        if c+a > 255:
            c = too_hi
            self.rgb[led.value] = c
        elif c+a < 0:
            c = too_lo
            self.rgb[led.value] = c
        else:
            c += a
            self.rgb[led.value] = c

        self.draw()

    def decrement(self, led: LED, amount=0, wrap_around=False):
        """
        Decreases the brightness of the specified LED by the specified amount.
        
        Parameters
        ------------------
        :param led: :class:`LED`
            specifies which LED should have its brightness decreased.
            
        :param amount: Optional[int]
            The amount by which the specified LED should decreased.

        :param wrap_around: Optional[boolean]
            Determines whether to set any values falling below zero to 255. Default is ``False``. Default behavior
            prevents any value from causing the color brightness to fall below zero.
        """
        self._keep_color()

        a = amount if amount is not 0 else self.increment_amount

        too_lo = 255 if wrap_around is True else 0
        too_hi = 0 if wrap_around is True else 255

        c = self.rgb[led.value]
        if c-a < 0:
            c = too_lo
            self.rgb[led.value] = c
        elif c-a > 255:
            c = too_hi
            self.rgb[led.value] = c
        else:
            c -= a
            self.rgb[led.value] = c

        self.draw()

    def set_led(self, led: LED, value: int):
        """
        Sets the specified LED to the specified brightness.
        
        Parameters
        ------------------
        :param led: :class:`LED`
            specifies which LED will have its brightness set.
            
        :param value: int
            Specifies the level to which the brightness will be set.
            Acceptable values are between 0 and 255.
        """
        self._keep_color()

        if value > 255:
            self.rgb[led.value] = 255
        elif value < 0:
            self.rgb[led.value] = 0
        else:
            self.rgb[led.value] = value

        self.draw()

    def set_color(self, r: int, g: int, b: int):
        """
        Sets the color of this pixel to the values specified.
        
        The acceptable range for all of these parameters is between 0 and 255 inclusive.
        
        Parameters
        ----------------
        :param r: int
            Specifies the brightness to which the red LED should be set.
            
        :param g: int
            Specifies the brightness to which the green LED should be set.
            
        :param b: int
            Specifies the brightness to which the blue LED should be set.
        """
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
        """
        Increments the overall brightness of this pixel by the specified amount.
        Similar to the :func:`increment` method, this method increases the brightness of the whole pixel by a specified
        scale factor.
        
        Parameters
        ------------------
        :param amount: Optional[float]
            The amount at which the brightness of this pixel will be increased.
            
            Acceptable values are between -1.0 and 1.0.
            
            If the brightness of the pixel drops below 0.05 the pixel will automatically turn off.
        """
        a = amount if amount != 0.0 else self.bi
        if self.brightness+a > 1.0:
            self.brightness = 1.0
        elif self.brightness+a < 0.0:
            self.brightness = 0
        else:
            self.brightness += a

        self.draw()

    def set_brightness(self, brightness):
        """
        Sets the total brightness of the pixel. Valid values are floats between ``0.0`` and ``1.0``.

        :param brightness: The value to which brightness is to be set.
        """
        if 0 <= brightness <= 1.0:
            self.brightness = brightness
        elif brightness >= 1.0:
            self.brightness = 1
        else:
            self.brightness = 0.0

        self.draw()
        
    def red(self):
        """
        Changes the color of this pixel to red.
        """
        self.set_led(LED.RED, 255)
        self.set_led(LED.GREEN, 0)
        self.set_led(LED.BLUE, 0)
        self.draw()
        
    def green(self):
        """
        Changes the color of this pixel to green.
        """
        self.set_led(LED.RED, 0)
        self.set_led(LED.GREEN, 255)
        self.set_led(LED.BLUE, 0)
        self.draw()
        
    def blue(self):
        """
        Changes the color of this pixel to blue.
        """
        self.set_led(LED.RED, 0)
        self.set_led(LED.GREEN, 0)
        self.set_led(LED.BLUE, 255)
        
    def flash(self, r=0, g=0, b=0, length=0.25):
        """
        Causes this pixel to flash once.
        
        If all of the color parameters (``r``, ``g``, and ``b``) Are zero, then sets this pixel to black and flashes the
        color that the pixel had been prior to calling this method.
        
        The values of the color parameters must be between ``0`` and ``255``.
        
        Parameters
        ------------------
        :param r: Optional[int]
            The brightness of the red LED to use in the flash.
            
        :param g: Optional[int]
            The brightness of the red LED to use in the flash.
            
        :param b: Optional[int]
            The brightness of the blue LED to use in the flash.
            
        :param length: Optional[float]
            The length of time in seconds over which the flash takes place.
            
            If the length parameter is omitted, it defaults to ``0.25`` (a quarter of a second).
        """
        thread = FlashThread(self, length)
        if r == 0 and g == 0 and b == 0:
            self.black()
            self.revert_color()
            self.draw()
            thread.start()
        else:
            self.set_color(r, g, b)
            thread.start()

    def blink(self, r=0, g=0, b=0, brightness=0.1, interval=0.05, duration=2.0):
        """
        Flashes this pixel repeatedly for the duration specified.
        
        This method does not allow users to specify the ratio for which the pixel should be on to the time which it
        should be off. For this reason, using this method is not recommended. For more advanced blinking options, see
        :meth:`start_blink` and :meth:`stop_blink`.
        
        Like :meth:`flash`, if no color parameters are specified, this method will flash between black and the current
        color.
        
        Parameters
        ------------------
        :param r: Optional[int]
            The brightness to which the red LED should be set for this blink sequence.
            
        :param g: Optional[int]
            The brightness to which the green LED should be set for this blink sequence.
            
        :param b: Optional[int]
            The brightness to which the blue LED should be set for this blink sequence.
            
        :param interval: Optional[float]
            The time between switching between an "on" state and an "off" state.
            
            An "on" state is when the pixel's color equals that specified in this method's parameters.
            
            An "off" state is when the pixel's color is anything except the color specified in this method's parameters.
            
            NOTE: When the pixel is in an "off" state, it is not necessarily black. It is only not the specified color.
            
            The interval for both "on" and "off" states is equal. That is, the time spent "on" will always equal the time
            spent "off".
            
            If this behavior is not ideal, see the methods :meth:`start_blink` and :meth:`stop_blink` for more advanced
            behavior.
            
        :param duration: Optional[float]
            The length of time in seconds during which this blink sequence will run.

        :param brightness: Optional[float]
            Sets the overall brightness of the pixel when blinking.

            NOTE: If you set the brightness of the pixel using this option, the brightness set by this argument will
            remain even after the pixel has finished blinking.

            **WARNING**: This option does nothing in versions prior to version 1.0.0.
        """
        thread = BlinkThread(self, interval, duration)

        if 0 <= brightness <= 1.0 and brightness != self.brightness:
            self.brightness = brightness

        if r == 0 and g == 0 and b == 0:
            self.black()
            self.revert_color()
            self.draw()
            thread.start()
        else:
            self.set_color(r, g, b)
            thread.start()

    def start_blink(self, r=0, g=0, b=0, brightness=0.1, on_length=0.05, off_length=0.1):
        """
        Starts a blink sequence. This sequence will not terminate until :meth:`stop_blink` is called.
        
        Unlike :meth:`blink`, this method allows the user to specify the time which the pixel will be on and off
        separately.
        
        Parameters
        ------------------
        :param r: Optional[int]
            The brightness to which the red LED will be set during this blink sequence.
            
        :param g: Optional[int]
            The brightness to which the green LED will be set during this blink sequence.
            
        :param b: Optional[int]
            The brightness to which the blue LED will be set during this blink sequence.
            
        :param brightness: Optional[int]
            The overall brightness of the whole pixel during this blink sequence.
            
            NOTE: Setting the brightness using this argument will carry over to the brightness that the pixel uses once
            it is finished blinking.

            **WARNING**: This option does nothing in versions prior to version 1.0.0.
            
        :param on_length: Optional[float]
            The length of time in seconds that the pixel will be on for each flash.
            
        :param off_length: Optional[float]
            The length of time in seconds that the pixel will be off between flashes.
        """
        thread = AdvancedBlinkThread(self, on_length, off_length)
        if 0 <= brightness <= 1.0 and brightness != self.brightness:
            self.brightness = brightness

        if r == 0 and g == 0 and b == 0:
            self.black()
            self.revert_color()
            self.blinking_thread = thread
            thread.start()
        else:
            self.set_color(r, g, b)
            self.blinking_thread = thread
            thread.start()

    def stop_blink(self):
        """
        Stops the running blink sequence if it was started using :meth:`start_blink`.
        """
        self.blinking_thread.stop()
        self.black()
