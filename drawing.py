## This module is deprecated and is not used for anything.
import threading, asyncio, time
##import collections.deque

class LEDDrawThread(threading.Thread):
    def __init__(self, board):
        super(LEDDrawThread, self).__init__()
        self.board = board
        self.loop = asyncio.get_event_loop()
        self.task_queue = asyncio.Queue()
        self.running = True

    def interrupt(self):
        self.running = False

    def resume(self):
        self.running = True

    def draw_pixel(self, pixel):
        self.task_queue.put_no_wait(pixel)

    async def start_loop(self):
        print('The event loop has started')
        while self.running:
            for p in iter(self.task_queue.get, None):
                blinkt.set_pixel(p.addr, p.rgb[LED.RED], p.rgb[LED.GREEN], p.rgb[LED.BLUE], brightness=p.brightness)
                blinkt.show()
##            await asyncio.sleep(0.05)

    def run(self):
        self.loop.run_until_complete(self.start_loop())
##        self.loop.run_forever()
