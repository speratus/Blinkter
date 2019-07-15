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
        self.pixel._revert_color()
        self.pixel.draw()

class BlinkThread(threading.Thread):

    def __init__(self, pixel, interval: float, duration: float):
        super().__init__()
        self.pixel = pixel
        self.interval = interval
        self.duration = duration
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        elapsed_time = 0.0
        while self.running:
            s_time = time.process_time()
            
            time.sleep(self.interval)
##            self.pixel._keep_color()
            l = threading.Lock()
##            l.acquire()
            self.pixel.revert_color()
##            l.release()
##            self.pixel.draw()

            e_time = time.process_time()
            elapsed_time += e_time - s_time
##            print(f'The listed elapsed time is {elapsed_time}')

            if elapsed_time > self.duration:
                break

class AdvancedBlinkThread(threading.Thread):
    def __init__(self, pixel, on_length: float, off_length: float):
        super().__init__()
        self.pixel = pixel
        self.on_time = on_length
        self.off_time = off_length
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            time.sleep(self.on_time)

            self.pixel.revert_color()

            time.sleep(self.off_time)

            self.pixel.revert_color()
