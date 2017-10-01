#!/usr/bin/python
# script to restart/shutdown a raspberry pi

import RPi.GPIO as GPIO
import time
import os
from subprocess import call
from datetime import datetime

buttonTime = None
shutdownSeconds = 3

# hack function creates file and tails the created file
# used for avoiding a while true loop here
# raw_input() would be nice but systemd doesn't like that
def loop():
	os.system('date > /tmp/piboot')
	os.system('tail -f /tmp/piboot')

# function to run when an interrupt is called
def shutdown(pin):
	global buttonTime

	if GPIO.input(pin):
		# button is down
		if buttonTime is None:
			buttonTime = datetime.now()
	else:
		# button is up
		if buttonTime is not None:
			elapsed = (datetime.now() - buttonTime).total_seconds()
			buttonTime = None
			if elapsed >= shutdownSeconds:
				# button pressed for 3 seconds then shutdown
				call(['shutdown', '-h', 'now'], shell=False)
			else:
				# if not then reboot
				call(['shutdown', '-r', 'now'], shell=False)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # set pin numbering to board numbering
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # set up pin 5 as an input
GPIO.add_event_detect(5, GPIO.BOTH, callback=shutdown, bouncetime=50) # set up an interrupt to look for button presses

loop() # run loop function to keep script running
