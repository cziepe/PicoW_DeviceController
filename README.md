# PicoW_DeviceController

## A Raspberry Pico W project used to control devices such as relays with an instant interrupt cancel ie. an IR beam that has broken. 
## Experimental bluetooth scanning that triggers when a device is in a certain range

### Background
So why did I create this project? Living in a rented accomodation with a cat without a cat flap meant that we weren't able to let her in or out when we/she wanted. 
A cat flap would have been a lot easier but when I came across the PicoW, I set myself up with a challange to create something that would open and close a window and let the cat in and out. 

3 months later I have a built prototype device that the cat has been successfully using. 

I built this project using a Raspberry Pico W. It can perform the following tasks 

- Microdot webserver with http calls to control the functions

- Control two relays via gpio pins

- Monitor input while the relays have been actuated. I use this for an IR beam that goes across the window. If broken, a safety feature is triggered and the functions are reversed - so to not crush the cat!

- Bluetooth scanning. Experimental. Our cat has a tracker which I discovered can be scanned which then returns the signal strength. If nearby for a set amount of time it will activate the relays.

- Fully async with immediate gpio output cancellation. No waiting for the current function to complete before the next task can run. Again I didn't want to crush the cat!

### Setting up this project on your Pico W

Of course you will need one Rasbperry Pico W 

Then you will need a copy of Micropython with bluetooth support. You can download it here - https://micropython.org/download/RPI_PICO_W/
There are instructions on the internet on how to install this on your pico 

### Config 

In wlan.py, at the top there is the following lines of code 

`def networkSettings():
    return { 'ssid' : '', 'password' : '' }`

Here you will need to enter your wifi network id and password inside the quotes

If you are scanning for a bluetooth device, there are some settings in bleScane.py

  `TARGET_DEVICE_NAME = ''
  RSSI_THRESHOLD = -95
  RSSI_CLOSED_OUTSIDE_THRESHOLD = -95
  RSSI_CLOSED_INSIDE_THRESHOLD = -75
  RSSI_OPENED_THRESHOLD = -75
  DURATION = 10`

In TARGET_DEVICE_NAME, you will need to find the id of your bluetooth device. There are a few signal strength settings, along with the duration in seconds, that it takes to activate the relays. 

### Internet

I don't recommend expsoing this over the internet directly. There is no security at all with the current configuration. In my set up I have this only available on my internal network only. 

I do have an internet facing device that controls the pico W. I built this using an old Raspberry PI Zero running apache, NOIP and LetsEncrypt. All open source and free services that allows me to have a secure https service with a free ssl certficate. I will expand on this at a later date. 





The project will then need to be copied in the same structure as the repository is in. 




