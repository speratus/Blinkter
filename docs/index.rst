.. blinkter documentation master file, created by
   sphinx-quickstart on Wed Jul 17 12:15:22 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. currentmodule:: blinkter

Welcome to blinkter's documentation!
====================================

What is Blinkter?
------------------
Blinkter is an API to use with the |pimoroni|_ led hat for the Raspberry Pi. It adds many features lacking from
the |blinkt|_ library provided by pimoroni. See the section below for a more complete list.

Features
--------
Here are some of the features that blinkter offers.

- Object oriented design

   * The original blinkt library is not object oriented
   * Object oriented design is particularly intuitive in the case of the pimoroni Blinkt! because the blinkt is actually
      an object.

- Super convenient methods for setting the pixels to the three basic colors (red, green, and blue).
- Adds a :meth:`~Pixel.flash` method for easy flashing.
- If you don't just want to flash LEDs, but you also want to blink them, you should check out the built in
   :meth:`~Pixel.start_blink` and :meth:`~Pixel.stop_blink` for more information.

Quick demonstration
-------------------
Cycle through the basic colors.::

    import time
    from blinkter import BlinktBoard

    board = BlinktBoard()
    pixel = board.get_pixel(0) #As with blinkt, the pixels are labelled 0-7.
    pixel.red()
    time.sleep(1)
    pixel.green()
    time.sleep(1)
    pixel.blue()
    time.sleep(3)
    pixel.black()  #Turn the pixel off when you're done.

Cause a pixel to flash once.::

    pixel.flash(r=255, duration=0.1)

Blink a pixel repeatedly::

    pixel.start_blink(g=255, on_length=0.075, off_length=0.2)
    time.sleep(3)
    pixel.stop_blink()



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   classes/BlinktBoard
   classes/Pixel
   classes/LED



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
