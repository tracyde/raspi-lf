#!/usr/bin/env python

# Connections to Raspberry Pi:
#
# L298N
#   IN1 = GPIO6  [Pin 31]
#   IN2 = GPIO5  [Pin 29]
#   IN3 = GPIO13 [Pin 33]
#   IN4 = GPIO12 [Pin 32]
#   ENA = GPIO16 [Pin 36]
#   ENB = GPIO26 [Pin 37]
#

# Needed modules will be imported and configured
import sys
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# Declaration of the input pins which are connected to the sensors
IN1_PIN = 6
IN2_PIN = 5
IN3_PIN = 13
IN4_PIN = 12
ENA_PIN = 16
ENB_PIN = 26

# IN1 | IN2 | ENA -- Controls Right Motor (Alias values)
RW_FWD = IN2_PIN
RW_BWD = IN1_PIN
RW_PWR = ENA_PIN

# IN3 | IN4 | ENB -- Controls Left Motor (Alias values)
LW_FWD = IN4_PIN
LW_BWD = IN3_PIN
LW_PWR = ENB_PIN

# Setup the declared pins
GPIO.setup(IN1_PIN, GPIO.OUT)
GPIO.setup(IN2_PIN, GPIO.OUT)
GPIO.setup(IN3_PIN, GPIO.OUT)
GPIO.setup(IN4_PIN, GPIO.OUT)
GPIO.setup(ENA_PIN, GPIO.OUT)
GPIO.setup(ENB_PIN, GPIO.OUT)

# Break between driving motors will be defined here (in seconds)
sleeptime=5

# Helper Functions
def forward(x):
    print("Moving Forward")
    GPIO.output(RW_PWR, GPIO.HIGH)
    GPIO.output(LW_PWR, GPIO.HIGH)
    GPIO.output(RW_FWD, GPIO.HIGH)
    GPIO.output(LW_FWD, GPIO.HIGH)
    time.sleep(x)
    print("Braking")
    GPIO.output(RW_BWD, GPIO.HIGH)
    GPIO.output(RW_BWD, GPIO.HIGH)
    time.sleep(0.5)
    print("Stopping")
    GPIO.output(RW_PWR, GPIO.LOW)
    GPIO.output(LW_PWR, GPIO.LOW)
    GPIO.output(RW_FWD, GPIO.LOW)
    GPIO.output(RW_BWD, GPIO.LOW)
    GPIO.output(LW_FWD, GPIO.LOW)
    GPIO.output(LW_BWD, GPIO.LOW)

def reverse(x):
    print("Moving Forward")
    GPIO.output(RW_PWR, GPIO.HIGH)
    GPIO.output(LW_PWR, GPIO.HIGH)
    GPIO.output(RW_BWD, GPIO.HIGH)
    GPIO.output(LW_BWD, GPIO.HIGH)
    time.sleep(x)
    print("Braking")
    GPIO.output(RW_FWD, GPIO.HIGH)
    GPIO.output(RW_FWD, GPIO.HIGH)
    time.sleep(0.5)
    print("Stopping")
    GPIO.output(RW_PWR, GPIO.LOW)
    GPIO.output(LW_PWR, GPIO.LOW)
    GPIO.output(RW_FWD, GPIO.LOW)
    GPIO.output(RW_BWD, GPIO.LOW)
    GPIO.output(LW_FWD, GPIO.LOW)
    GPIO.output(LW_BWD, GPIO.LOW)

# main program loop
try:
    while True:
        forward(1)
        reverse(1)
        print "---------------------------------------"
        # Reset + Delay
        time.sleep(sleeptime)
 
# Scavenging work after the end of the program
except KeyboardInterrupt:
    GPIO.cleanup()