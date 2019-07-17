import blinkt
import threading

from .pixel import *

class Singleton(type):
    """
    Represents a Singleton class.
    
    A Singleton is a class that can have only one instance in the entire environment in which it exists.
    
    Singleton is used purely as a metadata class. Don't instantiate it anywhere.
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class BlinktBoard(metaclass=Singleton):
    """
    Represents the pimoroni Blinkt! GPIO board. This class is a singleton because in order to ensure threadsafety,
    it has to make sure that there are no other instances of it present in the current execution environment.
    
    An instance of this class can be obtained in the following manner:
    .. code-block:: python3
        from blinkter import BlinktBoard
        board = BlinktBoard()
    """
    def __init__(self):
        self.pixels = []
        self.lock = threading.Lock()
        for i in range(8):
            self.pixels.append(Pixel(self, i))
##        self.thread = drawing.LEDDrawThread(self)
##        blinkt.set_brightness(0.0)
##        self.thread.start()

    def get_pixel(self, idx):
        """
        Returns a single :class:`Pixel` on the blinkt board.
        
        Parameters
        ------------------
        idx: int
            The index of the pixel to get.
        """
        return self.pixels[idx]
        
    def black_all(self):
        """
        Turns all the pixels on the blinkt board off.
        """
        self.lock.acquire()
        blinkt.clear()
        blinkt.show()
        self.lock.release()
