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
        self.pixel.revert_color()
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
                self.pixel.revert_color()
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
