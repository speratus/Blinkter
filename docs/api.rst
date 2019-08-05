.. py:currentmodule:: blinkter
API Reference
=============
This page contains all of the basic information about the Blinkter library. You should be able to find the answers to
most question you will have about the library here.

BlinktBoard
-----------
This class is the entry point for accessing the rest of the library.

.. autoclass:: BlinktBoard
   :members:

Pixel
-----
Most of Blinkter's features are accessed through this class.

- Easy color setting with the :meth:`~Pixel.black`, :meth:`~Pixel.white`, :meth:`~Pixel.red`, :meth:`~Pixel.green`, and :meth:`~Pixel.blue` methods.
- Custom colors via the :meth:`~Pixel.set_color` method.
- Flashing and blinking using the :meth:`~Pixel.flash`, and the :meth:`~Pixel.start_blink` methods.

.. autoclass:: Pixel
   :members:

LED
---
A utility class designed to make certain parameter calls more convenient. It is only necessary to be used in some of
:class:`Pixel`'s methods.

.. autoclass:: LED
   :members: