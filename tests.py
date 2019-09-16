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

#import blinkt
import sys
sys.modules['blinkt'] = mock.MagicMock()

from blinkter import BlinktBoard, Pixel, LED


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


if __name__ == '__main__':
    unittest.main()
