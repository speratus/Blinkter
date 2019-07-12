# README
Blinkter makes using the [Pimoroni Blinkt!](https://shop.pimoroni.com/products/blinkt) even  easier by making it object oriented and 
adding several convenience methods. The intuitive objects that Blinkter layers on top of the [Blinkt!](https://github.com/pimoroni/blinkt)
python library greatly improve ease of use and reduce development times.
# Installation
1. In order to install Blinkter, first make sure that `setuptools` is installed.
'''
pip install setuptools
'''
2. Next, clone this repository with
```
git clone https://github.com/speratus/Blinkter.git
```
3. Once you have the repository setup on your system, you will have to generate the installation files with `setuptools`.
Run the following command:
```
python setup.py sdist
```
4. Once `setup.py` finishes building the library, you can install it using this command:
```
python setup.py install
```
That's all there is to it. You should be ready to go in no time at all.

## Installing into a virtual environment.
Installing Blinkter into a virtual environment is not much harder than a regular installation of Blinkter.
Follow steps 1 through 3 as you normally would, but before executing step 4, make sure that your virtual environment is activated.
### Windows
On windows this is achieved using the command:
```
<ENVIRONMENT_NAME>\Scripts\activate
```
### Linux
In linux, the command is,
```
source <ENVIRONMENT_NAME>/bin/activate
```

Doing this will ensure that Blinkter is installed into the appropriate environment.

# Usage

