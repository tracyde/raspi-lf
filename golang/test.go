#!/usr/bin/env python

import time
 
print "Test Program [press ctrl+c to end]"
 
# main program loop
try:
    time.sleep(60)

# Scavenging work after the end of the program
except KeyboardInterrupt:
    print "Exiting program via Interrupt"
    exit