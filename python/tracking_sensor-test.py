#!/usr/bin/env python

# Connections to Raspberry Pi:
#
# Tracking Module 1:
#   Signal = GPIO17 [Pin 11]
#
# Tracking Module 2:
#   Signal = GPIO27 [Pin 13]
#
# Tracking Module 3:
#   Signal = GPIO22 [Pin 15]
#

# Needed modules will be imported and configured
import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
 
# Declaration of the input pins which are connected to the sensors
TM1_PIN = 17
TM2_PIN = 27
TM3_PIN = 22

# Setup the declared pins
GPIO.setup(TM1_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(TM2_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(TM3_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Break between the results will be defined here (in seconds)
delayTime = 0.5

# Helper Functions
def check_pin(mod, pin):
    if GPIO.input(pin) == True:
        on_line(mod)
    else:
        off_line(mod)

def on_line(mod):
    print "LineTracker: {} is on the line".format(mod)

def off_line(mod):
    print "Linetracker: {} is not on the line".format(mod)

print "Sensor-Test [press ctrl+c to end]"
 
# main program loop
try:
    while True:
        check_pin(1, TM1_PIN)
        check_pin(2, TM2_PIN)
        check_pin(3, TM3_PIN)
        print "---------------------------------------"
        # Reset + Delay
        time.sleep(delayTime)
 
# Scavenging work after the end of the program
except KeyboardInterrupt:
    GPIO.cleanup()