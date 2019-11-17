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

import unittest
import threading
from unittest import mock
from copy import deepcopy

#import blinkt
import sys
sys.modules['blinkt'] = mock.MagicMock()
import blinkt

from blinkter import BlinktBoard, Pixel, LED
from blinkter.threads import FlashThread, BlinkThread, AdvancedBlinkThread
import blinkter.threads


# class BasicPixelTests(unittest.TestCase):
#     def SetUp(self):
#         self.board = BlinktBoard()
#         self.pixel = self.board.get_pixel(0)

#    @mock.patch.object(threading.Lock, 'acquire', autospec=True)
#    @mock.patch.object(threading.Lock, 'release', autospec=True)
#    @mock.patch('blinkt.set_pixel', autospec=True)
#    @mock.patch('blinkt.show', autospec=True)
#    def test_draw_works(self, mock_show, mock_set, mock_release, mock_acquire):
#        self.pixel.green()
#        mock_acquire.assert_called()
#        mock_set.assert_called_with(0, 0, 255, 0, 0.1)
#        mock_show.assert_called()
#        mock_release.assert_called()


class ColorSettingTests(unittest.TestCase):
    def setUp(self):
        self.board = BlinktBoard()
        self.pixel = self.board.get_pixel(0)
        
    def test_correct_pixel(self):
        self.assertEqual(self.pixel.addr, 0, msg='The Pixel address was incorrect!')

    @mock.patch.object(Pixel, 'draw', autospec=True)
    def test_black(self, mock_draw):
        self.pixel.set_color(14, 14, 14)
        mock_draw.assert_called()
        self.pixel.black()
        black = [0, 0, 0]
        self.assertEqual(self.pixel.rgb, black, msg=f'pixel.black() failed. {self.pixel.rgb} did not equal {black}.')
        mock_draw.assert_called()

    @mock.patch.object(Pixel, 'draw', autospec=True)
    def test_white(self, mock_draw):
        self.pixel.white()
        mock_draw.assert_called()
        white = [255,255,255]
        self.assertEqual(self.pixel.rgb, white, msg=f'pixel.white() failed. {self.pixel.rgb} does not equal {white}.')

    @mock.patch.object(Pixel, 'draw', autospec=True)
    def test_red(self, mock_draw):
        self.pixel.red()
        mock_draw.assert_called()
        red = [255, 0, 0]
        self.assertEqual(self.pixel.rgb, red, msg=f'pixel.red() failed. {self.pixel.rgb} does not equal {red}.')

    @mock.patch.object(Pixel, 'draw', autospec=True)
    def test_green(self, mock_draw):
        self.pixel.green()
        mock_draw.assert_called()
        green = [0, 255, 0]
        self.assertEqual(self.pixel.rgb, green, msg=f'pixel.red() failed. {self.pixel.rgb} does not equal {green}.')

    @mock.patch.object(Pixel, 'draw', autospec=True)
    def test_blue(self, mock_draw):
        self.pixel.blue()
        mock_draw.assert_called()
        blue = [0, 0, 255]
        self.assertEqual(self.pixel.rgb, blue, msg=f'pixel.red() failed. {self.pixel.rgb} does not equal {blue}.')


class IncrementTests(unittest.TestCase):
    def setUp(self) -> None:
        self.board = BlinktBoard()
        self.pixel = self.board.get_pixel(0)
        self.pixel.black()
        self.cases = [
            (10, 10),
            (30, 40),
            (70, 110),
            # NOTE: The following test case revealed that pixel.increment() behaved in an unexpected way when exceeding
            #       the 255 value limit. Originally, trying to increment beyond the acceptable limit caused it to wrap
            #       around to zero, but for normalization purposes, I have changed that behavior. This change needs to
            #       be noted in the changelog.
            #       At some point in the future, I think it would be good to add the wrap around functionality back into
            #       the increment code, but it needs to be done using a parameter, and it should not wrap around by
            #       default.
            (255, 255),
            (-130, 125),
            (75, 200),
            (15, 215),
            (-400, 0),
            (9010, 255),
            (-230, 25),
            (100, 125),
            (-45, 80),
            (90, 170),
            (0, 180),
            (0, 190),
            (0, 200)
        ]

    def test_correct_pixel(self):
        self.assertEqual(self.pixel.addr, 0, msg='The pixel in IncrementTests was not set correctly.')

    @mock.patch.object(Pixel, 'draw', autospec=True)
    def test_increments(self, mock_draw):
        for c in self.cases:
            self.pixel.increment(LED.RED, amount=c[0])
            mock_draw.assert_called()
            self.assertEqual(self.pixel.rgb[0], c[1], msg=f'pixel.increment(LED.RED, amount={c[0]}) failed.')


class DecrementTests(unittest.TestCase):
    def setUp(self):
        self.board = BlinktBoard()
        self.pixel = self.board.get_pixel(0)
        self.cases = (
            (140, 115),
            (30, 85),
            (79, 6),
            # NOTE: Again, the following test revealed inconsistent wrap around behavior in pixel.decrement like the
            #       behavior in pixel.increment. I have removed this behavior for the time being and that needs to be
            #       noted in the changelog.
            (45, 0),
            (-50, 50),
            (-200, 250),
            (900, 0),
            (-678, 255),
            (0, 245),
            (80, 165),
            (-30, 195),
            (100, 95),
            (-5, 100),
            (0, 90),
            (0, 80),
            (0, 70),
            (15, 55)
        )

    def test_correct_pixel(self):
        self.assertEqual(self.pixel.addr, 0, msg='The pixel was not set correctly.')

    @mock.patch.object(Pixel, 'draw', autospec=True)
    def test_decrement(self, mock_draw):
        self.pixel.white()
        for c in self.cases:
            self.pixel.decrement(LED.RED, amount=c[0])
            self.assertEqual(self.pixel.rgb[0], c[1], msg=f'pixel.decrement(LED.RED, amount={c[0]}) failed.')
            mock_draw.assert_called()


class SetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.board = BlinktBoard()
        self.pixel = self.board.get_pixel(3)
        self.led_cases = (
            (LED.RED, 45, 45),
            (LED.GREEN, 98, 98),
            (LED.BLUE, 117, 117),
            (LED.BLUE, 430, 255),
            (LED.RED, 87, 87),
            (LED.GREEN, -125, 0),
            (LED.RED, 210, 210),
            (LED.BLUE, -2, 0),
            (LED.GREEN, 450, 255),
            (LED.RED, 256, 255),
            (LED.RED, 130, 130),
            (LED.GREEN, 73, 73),
            (LED.GREEN, 0, 0),
            (LED.GREEN, 255, 255),
            (LED.RED, 255, 255)
        )
        self.rgb_cases = (
            ((255, 0, 0), [255, 0, 0]),
            ((255, 255, 0), [255, 255, 0]),
            ((255, 255, 255), [255, 255, 255]),
            ((0, 255, 255), [0, 255, 255]),
            ((0, 0, 255), [0, 0, 255]),
            ((0, 0, 0), [0, 0, 0]),
            ((0, 255, 0), [0, 255, 0]),
            ((13, 45, 78), [13, 45, 78]),
            ((96, 85, 74), [96, 85, 74]),
            ((32, 65, 98), [32, 65, 98]),
            ((500, -456, 0), [255, 0, 0]),
            ((45, 257, -78), [45, 255, 0]),
            ((153, 210, 88), [153, 210, 88])
        )

    def test_correct_pixel(self):
        self.assertEqual(self.pixel.addr, 3, msg='The pixel was not set properly!')

    @mock.patch.object(Pixel, 'draw', autospec=True)
    def test_led_cases(self, mock_draw):
        for c in self.led_cases:
            self.pixel.set_led(c[0], c[1])
            self.assertEqual(self.pixel.rgb[c[0].value], c[2], msg=f'pixel.set_led() failed. color: {c[0].name}, value: {c[1]}.')
            mock_draw.assert_called()

    @mock.patch.object(Pixel, 'draw', autospec=True)
    def test_set_color(self, mock_draw):
        for c in self.rgb_cases:
            i = c[0]
            t = c[1]
            self.pixel.set_color(i[0], i[1], i[2])
            self.assertEqual(self.pixel.rgb, t, msg='pixel.set_color() failed.')
            mock_draw.assert_called()


class RevertTests(unittest.TestCase):
    def setUp(self) -> None:
        self.board = BlinktBoard()
        self.pixel = self.board.get_pixel(2)
        self.cases = (
            {'rgb': [255, 255, 255], 'orgb': [0, 0, 0]},
            {'rgb': [127, 127, 127], 'orgb': [255, 255, 255]},
            {'rgb': [0, 140, 233], 'orgb': [45, 90, 23]},
            {'rgb': [75, 125, 456], 'orgb': [-45, 34, 190]},
            {'rgb': [85, 65, 75], 'orgb': [39, 37, 35]}
        )

    @mock.patch.object(Pixel, 'draw', autospec=True)
    def test_revert_color(self, mock_draw):
        for c in self.cases:
            self.pixel.rgb[LED.RED.value] = c['rgb'][LED.RED.value]
            self.pixel.rgb[LED.GREEN.value] = c['rgb'][LED.GREEN.value]
            self.pixel.rgb[LED.BLUE.value] = c['rgb'][LED.BLUE.value]

            self.pixel.orgb[LED.RED.value] = c['orgb'][LED.RED.value]
            self.pixel.orgb[LED.GREEN.value] = c['orgb'][LED.GREEN.value]
            self.pixel.orgb[LED.BLUE.value] = c['orgb'][LED.BLUE.value]

            self.pixel.revert_color()

            self.assertEqual(c['orgb'], self.pixel.rgb, msg=f'self.pixel.rgb should be {c["orgb"]}, it is {self.pixel.rgb}')
            self.assertEqual(c['rgb'], self.pixel.orgb, msg=f'self.pixel.orgb should be {c["rgb"]}, it is {self.pixel.orgb}')


class FlashTests(unittest.TestCase):
    def setUp(self):
        self.board = BlinktBoard()
        self.pixel = self.board.get_pixel(4)
        self.cases = (
            {'r': 0, 'g': 0, 'b': 0, 'length': 0.25},
            {'r': 35, 'g': 255, 'b': 85, 'length': 0.57},
            {'r': 255, 'g': 255, 'b': 255, 'length': 2}
        )

    # NOTE: the following test may (should?) be revised at some point. Currently, all it tests (and all it is intended
    #       to test is whether everything is called properly. Even so, it could perhaps be organized in a better way.
    @mock.patch.object(FlashThread, 'start', autospec=True)
    @mock.patch.object(Pixel, 'set_color', autospec=True)
    @mock.patch.object(Pixel, 'draw', autospec=True)
    @mock.patch.object(Pixel, 'revert_color', autospec=True)
    @mock.patch.object(Pixel, 'black', autospec=True)
    def test_flash(self, mock_black, mock_revert, mock_draw, mock_set, mock_start):
        for c in self.cases:
            self.pixel.flash(r=c['r'], g=c['g'], b=c['b'], length=c['length'])

        self.assertEqual(1, mock_black.call_count, msg=f'pixel.black() was called {mock_black.call_count} times. It should have been called once.')
        self.assertEqual(len(self.cases), mock_start.call_count, msg=f'thread.start() was called {mock_start.call_count} times. It should have been called {len(self.cases)} times.')
        self.assertEqual(1, mock_revert.call_count, msg=f'pixel.revert_color() was called {mock_revert.call_count} times. It should have been called once.')
        self.assertEqual(2, mock_set.call_count, msg=f'pixel.set_color() was called {mock_set.call_count} times. It should have been called twice.')
        self.assertEqual(1, mock_draw.call_count, msg=f'pixel.draw() was called {mock_draw.call_count} times. It should have been called 11 times.')


class BlinkTests(unittest.TestCase):
    def setUp(self) -> None:
        self.board = BlinktBoard()
        self.pixel = self.board.get_pixel(5)
        self.cases = (
            {'r': 0, 'g': 0, 'b': 0, 'interval': 0.1, 'duration': 4},
            {'r': 46, 'g': 89, 'b': 57, 'interval': 0.01, 'duration': 1},
            {'r': 255, 'g': 255, 'b': 255, 'interval': 0.25, 'duration': 3},
            {'r': 0, 'g': 0, 'b': 0, 'interval': 0.1, 'duration': 10}
        )

    # @mock.patch.object(BlinkThread, '__init__', autospec=True)
    @mock.patch.object(BlinkThread, 'start', autospec=True)
    @mock.patch.object(Pixel, 'draw', autospec=True)
    @mock.patch.object(Pixel, 'set_color', autospec=True)
    @mock.patch.object(Pixel, 'black', autospec=True)
    @mock.patch.object(Pixel, 'revert_color', autospec=True)
    def test_blink(self, mock_revert, mock_black, mock_set, mock_draw, mock_start):  # , mock_init):
        for c in self.cases:
            self.pixel.blink(r=c['r'], g=c['g'], b=c['b'], interval=c['interval'], duration=c['duration'])
            #mock_init.assert_called_with(c['interval'], c['duration'])

        self.assertEqual(2, mock_revert.call_count, msg=f'pixel.revert_color() was called {mock_revert.call_count} times. It should have been called twice')
        self.assertEqual(2, mock_black.call_count, msg=f'pixel.black() was called {mock_black.call_count} times. It should have been called twice.')
        self.assertEqual(2, mock_set.call_count, msg=f'pixel.set_color() was called {mock_set.call_count} times. It should have been called twice.')
        self.assertEqual(2, mock_draw.call_count, msg=f'pixel.draw() was called {mock_draw.call_count} times. It should have been called twice.')
        self.assertEqual(len(self.cases), mock_start.call_count, msg=f'thread.start() was called {mock_start.call_count} times. It should have been called {len(self.cases)} times.')


class AdvancedBlinkTests(unittest.TestCase):
    def setUp(self):
        self.board = BlinktBoard()
        with mock.patch('blinkter.threads.AdvancedBlinkThread', autospec=True):
            self.pixel = self.board.get_pixel(1)
        self.cases = (
            {'r': 0, 'g': 0, 'b': 0, 'on_length': 0.05, 'off_length': 0.1},
            {'r': 45, 'g': 59, 'b': 200, 'on_length': 0.1, 'off_length': 0.05},
            {'r': 255, 'g': 87, 'b': 255, 'on_length': 0.006, 'off_length': 1},
            {'r': 255, 'g': 255, 'b': 255, 'on_length': 1, 'off_length': 0.2},
            {'r': 0, 'g': 0, 'b': 0, 'on_length': 0.01, 'off_length': 0.01}
        )

    @mock.patch.object(Pixel, 'black', autospec=True)
    @mock.patch.object(Pixel, 'revert_color', autospec=True)
    @mock.patch.object(AdvancedBlinkThread, 'start', autospec=True)
    @mock.patch.object(Pixel, 'set_color', autospec=True)
    def test_advanced_blink(self, mock_set, mock_start, mock_revert, mock_black):
        for c in self.cases:
            self.pixel.start_blink(r=c['r'], g=c['g'], b=c['b'], on_length=c['on_length'], off_length=c['off_length'])

        self.assertEqual(3, mock_set.call_count, msg=f'pixel.set_color() was not called the correct number of times.')
        self.assertEqual(2, mock_revert.call_count, msg=f'pixel.revert_color() was not called the correct number of times.')
        self.assertEqual(2, mock_black.call_count, msg=f'pixel.black() was not called the correct number of times.')
        self.assertEqual(len(self.cases), mock_start.call_count, msg=f'AdvancedBlinkThread.start() was not called {len(self.cases)} times.')

    @mock.patch.object(Pixel, 'black', autospec=True)
    @mock.patch.object(AdvancedBlinkThread, 'stop', autospec=True)
    def test_stop_blink(self, mock_stop, mock_black):
        self.pixel.stop_blink()
        mock_stop.assert_called()
        mock_black.assert_called()


class BlinktBoardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.board = BlinktBoard()

    #@mock.patch.object(threading.Lock, 'acquire', autospec=True)
    @mock.patch('blinkt.clear', autospec=True)
    @mock.patch('blinkt.show', autospec=True)
    def test_black_all(self, mock_show, mock_clear):
        self.board.black_all()
        mock_show.assert_called()
        mock_clear.assert_called()
        #mock_acquire.assert_called()


class BlinkSleepHelper:

    def __init__(self, interval, duration):
        self.counter = 0
        self.normalized = duration / interval

    def next(self):
        self.counter += 1
        return self.counter


class BlinkThreadTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cases = (
            (0.01, 2.0),
            (0.02, 4.0),
            (0.5, 1.25)
        )
        self.pixel = BlinktBoard().get_pixel(0)

    @mock.patch('blinkter.threads.time.sleep', return_value=None)
    def test_blink(self, mock_sleep):
        for c in self.cases:
            helper = BlinkSleepHelper(c[0], c[1])
            blinkter.threads.time.process_time = helper.next

            self.pixel.red()
            start_color = deepcopy(self.pixel.orgb)
            thread = BlinkThread(self.pixel, c[0], helper.normalized)
            thread.run()

            self.assertEqual(start_color, self.pixel.rgb)


class AdvancedBlinkThreadTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cases = (
            (10, 0.1, 0.2),
            (15, 0.3, 0.7),
            (45, 0.02, 1.0),
            (300, 0.5, 0.6),
            (127, 0.1, 0.04),
            (73, 0.4, 0.09)
        )
        self.pixel = BlinktBoard().get_pixel(3)

    def test_advanced_blink(self):
        class SleepHelper:
            def __init__(self, blink_count: int, thread: AdvancedBlinkThread):
                self.call_num = blink_count
                self.counter = 0
                self.called_with = []
                self.thread = thread

            def next(self, time):
                if time not in self.called_with:
                    self.called_with.append(time)
                self.counter += 1

                if self.counter >= self.call_num:
                    self.thread.stop()

        for c in self.cases:
            thread = AdvancedBlinkThread(self.pixel, c[1], c[2])
            helper = SleepHelper(c[0], thread)
            blinkter.threads.time.sleep = helper.next

            self.pixel.green()
            start_color = deepcopy(self.pixel.orgb)
            thread.run()

            self.assertEqual(start_color, self.pixel.rgb)
            self.assertEqual([c[1], c[2]], helper.called_with)


class BrightnessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.set_cases = (
            (0.9, 0.9),
            (35, 1.0),
            (0, 0),
            (0.03, 0.03),
            (-68, 0)
        )
        self.pixel = BlinktBoard().get_pixel(4)
        self.inc_cases = (
            (0, 0.2),
            (0.4, 0.6),
            (0.5, 1.0),
            (-0.5, 0.5),
            (-0.7, 0.0),
            (0, 0.1),
            (0.5, 0.6)
        )

    def test_set(self):
        for c in self.set_cases:
            self.pixel.set_brightness(c[0])

            self.assertEqual(c[1], self.pixel.brightness)

    def test_inc(self):
        for c in self.inc_cases:
            self.pixel.increment_brightness(c[0])

            self.assertAlmostEqual(self.pixel.brightness, c[1])


if __name__ == '__main__':
    unittest.main()
