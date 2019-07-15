import blinkt
import threading

from .pixel import *

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class BlinktBoard(metaclass=Singleton):
    def __init__(self):
        self.pixels = []
        self.lock = threading.Lock()
        for i in range(8):
            self.pixels.append(Pixel(self, i))
##        self.thread = drawing.LEDDrawThread(self)
##        blinkt.set_brightness(0.0)
##        self.thread.start()

    def get_pixel(self, idx):
        return self.pixels[idx]
        
    def black_all(self):
        self.lock.acquire()
        blinkt.clear()
        blinkt.show()
        self.lock.release()
