#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

rotaryDialOutWhite = 20 # Broadcom pin 20
rotaryDialOutYellow = 21 # Broadcom pin 21
rotaryDialInGreen = 5 # Broadcom pin 5
rotaryDialInBrown = 6 # Broadcom pin 6

try:
  print("Initializing GPIO ports.")
  rotating = False
  pulsCount = 0
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(rotaryDialOutWhite, GPIO.OUT)
  GPIO.setup(rotaryDialOutYellow, GPIO.OUT)
  GPIO.setup(rotaryDialInGreen, GPIO.IN)
  GPIO.setup(rotaryDialInBrown, GPIO.IN)

  GPIO.output(rotaryDialOutWhite, GPIO.HIGH)
  GPIO.output(rotaryDialOutYellow, GPIO.HIGH)

  print("Ports initialized, waiting for dial pulses.")
  print("")

  #Dial Pulse
  def processDialPulse(param):
    if GPIO.input(rotaryDialInGreen) == GPIO.LOW:
       print("Puls detected")
       if(rotating):
         global pulsCount
         pulsCount += 1
    
  #RotatingDial
  def processRotatingDial(param):
    global pulsCount
    global rotating
    if GPIO.input(rotaryDialInBrown):
       print("Rotary dial turns")
       rotating = True
    else:   
       print("Dial no longer rotates")
       print("Number of pulses: ", pulsCount)
       print("")
       rotating = False
       pulsCount = 0

  GPIO.add_event_detect(rotaryDialInGreen, GPIO.FALLING, callback=processDialPulse, bouncetime=50 )
  GPIO.add_event_detect(rotaryDialInBrown, GPIO.BOTH, callback=processRotatingDial, bouncetime=50)

  while True:
     #checkStateGreen(None)
     #checkStateBrown(None)
     time.sleep(10)
  
except KeyboardInterrupt:
    print("Program aborted")
  
except Exception as error:
    print("Error or exception occurred, aborting program", error)
  
finally:
    GPIO.cleanup() # this ensures a clean exit