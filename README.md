# Bluetooth Login Using Raspberry Pi 

_Because your just that lazy!_

## What is Bluetooth Login? 
Bluetooth Login is a program that allows the user to log into the Alexa/Amazon Echo Jarvis skill using only
the Bluetooth connection on your phone!

## Installation
1. [Set up your Raspberry Pi with Raspbian](https://www.raspberrypi.org/documentation/setup/) 
1. Connect the Raspberry Pi to your local wifi network
1. Plug in your Bluetooth adapter to the Raspberry Pi. (Note: if you hava a R-pi 3 skip this step)
1. Install dependencies on Raspberry Pi
1. Create a folder called main in the 'pi' directory (Or other user directory if you aren't using the default user)
1. Clone this repository to the main directory 
1. In the BluetoothLogin directory create a directory called 'logs'
1. Run the 'set_startup_script.sh' script as root
1. Use the 'register_phone.py' script to register users for Bluetooth Login
1. Restart the raspberry pi and start using Bluetooth Login! 

## Using Bluetooth Login 
First register your phone with the 'register_phone.py' script.
 - Takes Bluetooth mac address
 - Takes Username of your chosing
 - Note: Must be unique and not in use by other user
Turn your Phones Bluetooth on and you are ready to use Bluetooth Login.

## Dependencies
 - python-dev
 - libbluetooth-dev
 - PyBluez
