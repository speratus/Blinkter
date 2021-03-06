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

from setuptools import setup, find_packages
import re


def get_property(prop, project):
    with open(project + '/__init__.py', 'r') as f:
        r = re.search(r'^{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), f.read(), re.MULTILINE)
        o = r.group(1)
        return o

with open('README.md', 'r') as fh:
    long_description = fh.read()

project_name = 'blinkter'

setup(
    name=project_name,
    version=get_property('__version__', project_name),
    packages=find_packages(),
    install_requires=['blinkt >= 0.1.2'],
    author='Andrew Luchuk',
    project_urls={
        'Documentation': 'http://blinkter.readthedocs.io/',
        'Issue tracker': 'https://github.com/speratus/Blinkter/issues'
    },
    author_email='spaxumof@gmail.com',
    description='A high level library for interacting with the Pimoroni Blinkt.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/speratus/Blinkter',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ]
)
