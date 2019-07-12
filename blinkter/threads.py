import threading
import time

##from .pixel import Pixel

class FlashThread(threading.Thread):
    
    def __init__(self, pixel, length: float):
        super().__init__()
        self.pixel = pixel
        self.length = length
        
    def run(self):
        time.sleep(self.length)
        pixel._revert_color()
        pixel.draw()
