#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

bellRingCtl = 17 # Broadcom pin 17 (P1 pin 11)

try:  
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(bellRingCtl, GPIO.OUT)

  def wecker():
    GPIO.output(bellRingCtl, GPIO.LOW)
    time.sleep(60)

  while True:
    wecker()
  
except KeyboardInterrupt:      
    print("Program aborted")
  
except:      
    print("Error or exception occurred, aborting program")  
  
finally:  
    GPIO.cleanup() # this ensures a clean exit  