# BluetoothLogin
_Because your just that lazy!_

##What it is
BluetoothLogin is a tool that allows you to log into the JarvisLabAssistant Alexa skill with just your phone and a bluetooth connection. 
This can be ported to work with other programs. All you need to do is change the action function

##How it works
This program works by scanning the network for open bluetooth devices and 
checking if the phones are registered in a ermrest database. It will choose the 
registered device that is the closest or has the most reliable connection and log them
into the database where the current user for JarvisLabAssistant is held.

##How to use
Set up a Raspberry Pi 3(or other rpi but you will require a bluetooth adapter) with Raspbian 
and clone this repository to your machine. Download the dependencies below and create a logs directory.
Set up your pi so that on launch to run bluetooth login.py scirpt will run.

##Dependencies
pi-bluetooth
pyvona(account required)
PyBluez
