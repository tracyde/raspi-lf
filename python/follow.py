#!/usr/bin/env python

# Connections to Raspberry Pi:
#
# Physical Layout
#
#      Front
#      3 2 1
#     /-----\
#    /_     _\
#    O |   | O
#      |   |
#    O_|   |_O
#    \       /
#     \-----/
#
#      Back
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
# L298N
#   IN1 = GPIO6  [Pin 31]
#   IN2 = GPIO5  [Pin 29]
#   IN3 = GPIO13 [Pin 33]
#   IN4 = GPIO12 [Pin 32]
#   ENA = GPIO16 [Pin 36]
#   ENB = GPIO26 [Pin 37]
#

# Needed modules will be imported and configured
import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
 
# Declaration of the input pins which are connected to the sensors
TM1_PIN = 17
TM2_PIN = 27
TM3_PIN = 22

IN1_PIN = 6
IN2_PIN = 5
IN3_PIN = 13
IN4_PIN = 12
ENA_PIN = 16
ENB_PIN = 26

# Setup the declared pins
GPIO.setup(TM1_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(TM2_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(TM3_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setup(IN1_PIN, GPIO.OUT)
GPIO.setup(IN2_PIN, GPIO.OUT)
GPIO.setup(IN3_PIN, GPIO.OUT)
GPIO.setup(IN4_PIN, GPIO.OUT)
GPIO.setup(ENA_PIN, GPIO.OUT)
GPIO.setup(ENB_PIN, GPIO.OUT)

# IN1 | IN2 | ENA -- Controls Right Motor (Alias values)
RW_FWD = IN2_PIN
RW_BWD = IN1_PIN
RW_ENA = GPIO.PWM(ENA_PIN, 100)

# IN3 | IN4 | ENB -- Controls Left Motor (Alias values)
LW_FWD = IN4_PIN
LW_BWD = IN3_PIN
LW_ENA = GPIO.PWM(ENB_PIN, 100)

# Go ahead and start the PWM
RW_ENA.start(0)
LW_ENA.start(0)

# Break between the results will be defined here (in seconds)
delayTime = 0.5

# Helper Functions
def check_pin(pin):
    if GPIO.input(pin) == True:
        return True
    else:
        return False

def forward():
    print("Moving Forward")
    RW_ENA.ChangeDutyCycle(50)
    LW_ENA.ChangeDutyCycle(50)
    GPIO.output(RW_FWD, GPIO.HIGH)
    GPIO.output(RW_BWD, GPIO.LOW)
    GPIO.output(LW_FWD, GPIO.HIGH)
    GPIO.output(LW_BWD, GPIO.LOW)

def right():
    print("Turning Right")
    RW_ENA.ChangeDutyCycle(50)
    LW_ENA.ChangeDutyCycle(50)
    GPIO.output(RW_FWD, GPIO.LOW)
    GPIO.output(RW_BWD, GPIO.HIGH)
    GPIO.output(LW_FWD, GPIO.HIGH)
    GPIO.output(LW_BWD, GPIO.LOW)

def left():
    print("Turning Left")
    RW_ENA.ChangeDutyCycle(50)
    LW_ENA.ChangeDutyCycle(50)
    GPIO.output(RW_FWD, GPIO.HIGH)
    GPIO.output(RW_BWD, GPIO.LOW)
    GPIO.output(LW_FWD, GPIO.LOW)
    GPIO.output(LW_BWD, GPIO.HIGH)

def stop():
    print("Stopping")
    RW_ENA.ChangeDutyCycle(0)
    LW_ENA.ChangeDutyCycle(0)
    GPIO.output(RW_FWD, GPIO.LOW)
    GPIO.output(LW_FWD, GPIO.LOW)
    GPIO.output(RW_BWD, GPIO.LOW)
    GPIO.output(LW_BWD, GPIO.LOW)

def cleanup():
    stop()
    RW_ENA.stop()
    LW_ENA.stop()
    GPIO.cleanup()

print "Naive Line Follower [press ctrl+c to end]"
 
# main program loop
try:
    complete = False
    while not complete:
        if check_pin(TM2_PIN):
            print("Found line")
            forward()
        elif check_pin(TM3_PIN):
            print("Turn Left")
            while check_pin(TM3_PIN):
                left()
        elif check_pin(TM1_PIN):
            print("Turn Right")
            while check_pin(TM1_PIN):
                right()
        #
        #elif check_pin(TM1_PIN) and check_pin(TM2_PIN) and check_pin(TM3_PIN):
        #    print("Stopping our run")
        #    complete = True
        else:
            print("Unable To Find Line... Stopping")
            stop()
        
        # Reset + Delay
        time.sleep(delayTime)

    # Run is over
    cleanup()

# Scavenging work after the end of the program
except KeyboardInterrupt:
    cleanup()