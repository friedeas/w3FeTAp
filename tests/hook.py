#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

hookIn1 = 23 # Broadcom pin 23
hookIn2 = 24 # Broadcom pin 24
hookOut = 25 # Broadcom pin 24

try:
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(hookIn1, GPIO.IN)
  GPIO.setup(hookIn2, GPIO.IN)
  GPIO.setup(hookOut, GPIO.OUT)
  GPIO.output(hookOut, GPIO.HIGH)

  def checkState(param):
    if GPIO.input(hookIn1):
        print("HookIn 1 is high => The receiver is picked up")
    if GPIO.input(hookIn2):
        print("HookIn 2 is high => The receiver is on the hook")    

  GPIO.add_event_detect(hookIn1, GPIO.BOTH, callback=checkState, bouncetime=200 )

  while True:
     checkState(None)
     time.sleep(5)
  
except KeyboardInterrupt:      
    print("Program aborted")
  
except Exception as error:
    print("Error or exception occurred, aborting program", error)  
  
finally:  
    GPIO.cleanup() # this ensures a clean exit  