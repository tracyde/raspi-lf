#!/usr/bin/env python

# Connections to Raspberry Pi:
# Signal = GPIO24 [Pin 18]
# +V     = 5V	  [Pin 4]
# GND    = GND    [Pin 6]

# Needed modules will be imported and configured
import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
 
# Declaration of the input pin which is connected with the sensor
GPIO_PIN = 24
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
 
# Break between the results will be defined here (in seconds)
delayTime = 0.5
 
print "Sensor-Test [press ctrl+c to end]"
 
# main program loop
try:
        while True:
            if GPIO.input(GPIO_PIN) == True:
                print "LineTracker is on the line"
            else:
                print "Linetracker is not on the line"
            print "---------------------------------------"
 
            # Reset + Delay
            time.sleep(delayTime)
 
# Scavenging work after the end of the program
except KeyboardInterrupt:
        GPIO.cleanup()