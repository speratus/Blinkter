.. currentmodule:: blinkter

LED
===
Represents the possible LEDs in an individual pixel. This class needs only
be used in methods of the :class:`Pixel` class.

.. autoclass:: LED
   :members:

Usage
-----
This enumeration is intended to be used in a very limited set of circumstances. Its main purpose is to serve as a
convenience class for certain operations inside the :class:`Pixel` class. Given the limited scope of its usefulness,
it may be removed in the future.

**Example:** ::
   ...
   #Code for obtaining a Pixel class
   pixel.set_led(LED.GREEN, 100)
   ...

