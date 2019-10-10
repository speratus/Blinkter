# README
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/blinkter.svg)
[![Documentation Status](https://readthedocs.org/projects/blinkter/badge/?version=latest)](https://blinkter.readthedocs.io/en/latest/?badge=latest)
[![GitHub release](https://img.shields.io/github/release/speratus/Blinkter.svg)](https://github.com/speratus/Blinkter/releases/tag/0.1.5.4)
[![PyPI](https://img.shields.io/pypi/v/blinkter.svg?color=green)](https://pypi.org/project/blinkter/)
[![GitHub license](https://img.shields.io/github/license/speratus/Blinkter.svg)](https://github.com/speratus/Blinkter/blob/master/LICENSE)
[![codecov](https://codecov.io/gh/speratus/Blinkter/branch/master/graph/badge.svg)](https://codecov.io/gh/speratus/Blinkter)
[![Build Status](https://travis-ci.org/speratus/Blinkter.svg?branch=master)](https://travis-ci.org/speratus/Blinkter)

[![Gitter](https://badges.gitter.im/raspberrypi-blinkter/community.svg)](https://gitter.im/raspberrypi-blinkter/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![Discord](https://img.shields.io/discord/610943654806159453?label=discord&logo=discord)](https://discord.gg/YqRfXwJ)

Blinkter makes using the [Pimoroni Blinkt!](https://shop.pimoroni.com/products/blinkt) even  easier by making the library object oriented and 
adding several convenience methods. The intuitive objects that Blinkter layers on top of the [Blinkt!](https://github.com/pimoroni/blinkt)
python library greatly improve ease of use and reduce development times.
# Installation

## Easy Way
```
pip install blinkter
```
## Harder way
If you want to play around with the Blinkter code, the following steps will guide you through getting the repository
and installing the library from your code.

1. Make sure that `setuptools` is installed.
```
pip install setuptools
```
2. Next, clone this repository with
```
git clone https://github.com/speratus/Blinkter.git
```

3. Once the repository is downloaded, install it using this command:
```
python setup.py install
```
That's all there is to it. You should be ready to go in no time at all.

## Installing into a virtual environment.
Installing Blinkter into a virtual environment is not much harder than a regular installation of Blinkter.
Follow steps 1 and 2 as you normally would, but before executing step 3, make sure that your virtual environment is activated.

### Linux
In linux (and Raspbian), the command is,
```
source <ENVIRONMENT_NAME>/bin/activate
```
### Windows
On windows this is achieved using the command:
**NOTE:** *Blinkter will not run on Windows. It works exclusively on the Raspberry pi.*
```
<ENVIRONMENT_NAME>\Scripts\activate
```

Doing this will ensure that Blinkter is installed into the appropriate environment.

# Usage
```python
import blinkter

board = blinkter.BlinktBoard()
pixel = board.get_pixel(0)  #Or whatever pixel you want to manipulate
pixel.red() #Or pixel.blue(), or whatever else you want.
```

# Discussion

You can ask questions on the [Discord Server](https://discord.gg/YqRfXwJ) or the [Gitter chat room](https://gitter.im/raspberrypi-blinkter/community?utm_source=share-link&utm_medium=link&utm_campaign=share-link).

# Links
* [Pimoroni Blinkt! product page](https://shop.pimoroni.com/products/blinkt)
* [Blinkt library](https://github.com/pimoroni/blinkt)
* [Documentation](https://blinkter.readthedocs.io/)
