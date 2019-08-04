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

import blinkt

from blinkter import BlinktBoard, Pixel, LED


class BasicPixelTests(unittest.TestCase):
    def SetUp(self):
        self.board = BlinktBoard()
        self.pixel = self.board.get_pixel(0)

    @mock.patch.object(threading.Lock, 'acquire', autospec=True)
    @mock.patch.object(threading.Lock, 'release', autospec=True)
    @mock.patch('blinkt.set_pixel', autospec=True)
    @mock.patch('blinkt.show', autospec=True)
    def test_draw_works(self, mock_show, mock_set, mock_release, mock_acquire):
        self.pixel.green()
        mock_acquire.asser_called()
        mock_set.assert_called_with(0, 0, 255, 0, 0.1)
        mock_show.assert_called()
        mock_release.assert_called()


if __name__ == '__main__':
    unittest.main()