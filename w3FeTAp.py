#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import os
import subprocess
import threading
import traceback
from audio.tones import DialTone

class Watchdog():
  
  def __init__(self, timeout):
    self.timeout = timeout
    self.expired = False
    self.cancelled = False
    self._t = None

  def do_expire(self):
    self.expired = True

  def _expire(self):
    print("\nWatchdog expire")
    self.do_expire()

  def start(self):
    self.cancelled = False
    if self._t is None:
      self._t = threading.Timer(self.timeout, self._expire)
      self.expired = False
      self._t.start()
    else:
      self.refresh()

  def stop(self):
    if self._t is not None:
      self._t.cancel()
      self._t = None
      self.expired = False

  def refresh(self):
    if self._t is not None:
      self.stop()
      self.start()

  def cancel(self):
    self.cancelled = True

# Hook Pins
hookIn1 = 23 # Broadcom pin 23
hookIn2 = 24 # Broadcom pin 24
hookOut = 25 # Broadcom pin 24

# Rotary Dial Pins
rotaryDialOutWhite = 20 # Broadcom pin 20
rotaryDialOutYellow = 21 # Broadcom pin 21
rotaryDialInGreen = 5 # Broadcom pin 5
rotaryDialInBrown = 6 # Broadcom pin 6

# Bell Ring Ctl.
bellRingCtl = 17 # Broadcom pin 17

#State identified by the hook switch
receiverIsInTheCradle = False

#Global variables for the rotating dial
rotating = False
pulsCount = 0

#Global variable for the dailing state
dailWatchdogTimeout = 4
dailing = False
numberToDail = ""
watchdog = Watchdog(dailWatchdogTimeout)

#Speed Dial Dictionary
# 1 = **610 = Intern
# TODO Remove numbers
speedDialDictionary = {'1': '**610', '2': '015234531542', '3': '015560494578'}

dialTone = None

try:
  def updateHookState (param):
    global receiverIsInTheCradle
    global dialTone
    global watchdog
    if GPIO.input(hookIn1):
        print("HookIn 1 is high => The receiver is picked up")
        receiverIsInTheCradle = False
    if GPIO.input(hookIn2):
        print("HookIn 2 is high => The receiver is in the cradle")
        watchdog.cancel()
        receiverIsInTheCradle = True
        if(dialTone is not None):
            dialTone.stop()

  def ringTheBell(state):
    GPIO.output(bellRingCtl, state)

  #Dial Pulse
  def processDialPulse(param):
    global watchdog
    if GPIO.input(rotaryDialInGreen) == GPIO.LOW:
       #print("Puls detected")
       if(dailing):
         watchdog.refresh()
       if(rotating):
         global pulsCount
         pulsCount += 1

  #RotatingDial
  def processRotatingDial(param):
    global dailing
    global pulsCount
    global rotating
    global numberToDail
    global watchdog
    global dialTone
    if GPIO.input(rotaryDialInBrown):
      print("Rotary dial turns")
      rotating = True
      dialTone.stop()
    else:   
      print("Dial no longer rotates")       
      rotating = False
      if(dailing):
        print("Number of pulses: ", pulsCount)
        print("")
        numberString = str(pulsCount)
        if('10' == numberString):
          numberString = '0'
        if(len(numberToDail) == 0):
          watchdog.start()
        numberToDail = numberToDail + numberString
        pulsCount = 0

  def dialnumber():
    print("Switching to dailing state")    
    global dailing
    global watchdog
    global numberToDail
    global dialTone
    dailing = True
    dialTone.play()
    numberToDail = ""
    print("Reset dail watchdog")
    watchdog = Watchdog(dailWatchdogTimeout)
    print("Watchdog state: " + str(watchdog.expired))
    while not watchdog.expired and not watchdog.cancelled:
      time.sleep(0.0001)
    return numberToDail
  
  def answerCall():
    if(not receiverIsInTheCradle):
      os.system("linphonecsh generic \"answer $(linphonecsh generic 'calls' | sed -n 4p | awk '{print $1}')\"")
      time.sleep(0.0001)

  def hangup():
    if(receiverIsInTheCradle):
        os.system('linphonecsh generic terminate')
        time.sleep(0.0001)

  def initLinphone():
    print("Trying initialize linphonecsh")
    result = subprocess.run(["./initPhone.sh"], shell=True, capture_output=True, text=True)
    print(result.stdout)
    print("Linphone initialized")

  def init():
    print("Initializing GPIO ports and event listener.")

    # Use BCM numbering
    GPIO.setmode(GPIO.BCM)

    # Init bell ring ctl
    GPIO.setup(bellRingCtl, GPIO.OUT)

    # Init the rotary dial pins
    GPIO.setup(rotaryDialOutWhite, GPIO.OUT)
    GPIO.setup(rotaryDialOutYellow, GPIO.OUT)
    GPIO.setup(rotaryDialInGreen, GPIO.IN)
    GPIO.setup(rotaryDialInBrown, GPIO.IN)
    GPIO.output(rotaryDialOutWhite, GPIO.HIGH)
    GPIO.output(rotaryDialOutYellow, GPIO.HIGH)

    # Init hook switch pins
    GPIO.setup(hookIn1, GPIO.IN)
    GPIO.setup(hookIn2, GPIO.IN)
    GPIO.setup(hookOut, GPIO.OUT)
    GPIO.output(hookOut, GPIO.HIGH)

    # Init hook switch event listener
    GPIO.add_event_detect(hookIn1, GPIO.BOTH, callback=updateHookState, bouncetime=200)
    # Init rotary dial event listener
    GPIO.add_event_detect(rotaryDialInGreen, GPIO.FALLING, callback=processDialPulse, bouncetime=50 )
    GPIO.add_event_detect(rotaryDialInBrown, GPIO.BOTH, callback=processRotatingDial, bouncetime=50)

    print("GPIO initializing completed")
    updateHookState(None)
    global dialTone
    dialTone = DialTone()
    initLinphone()

  def w3FeTAp():
    init()
    while True:
      if(receiverIsInTheCradle):        
        RINGCHECK = 'linphonecsh generic \'calls\' | sed -n 4p'
        line4 = subprocess.check_output(['bash', '-c', RINGCHECK ]).decode().strip()                
        if("IncomingReceived" in line4):
          #print("Incoming call")
          ringTheBell(GPIO.LOW)
          time.sleep(0.0001)
        else:
          ringTheBell(GPIO.HIGH)
      else:
        ringTheBell(GPIO.HIGH)
        CMD = 'linphonecsh generic "answer $(linphonecsh generic \'calls\' | sed -n 4p | awk \'{print $1}\')"'
        VALUE = subprocess.check_output(['bash', '-c', CMD ]).decode().strip()
        if VALUE == 'There are no calls to answer.':
          phoneNumber = dialnumber()
          if(len(phoneNumber) > 0):
            if(len(phoneNumber) == 1):
              speedDialNumber = speedDialDictionary.get(phoneNumber)              
              if(speedDialNumber is not None):
                print("Speed dial number " + speedDialNumber + " for " + phoneNumber)
                phoneNumber = speedDialNumber
            print("Dailing phone number: " + phoneNumber)
            os.system('linphonecsh dial ' + phoneNumber)
          else:
            print("No number to dail")
        else:
          answerCall()
        while not receiverIsInTheCradle:
          time.sleep(0.001)
        else:
          hangup()
      time.sleep(0.0001)

  w3FeTAp()
    
except KeyboardInterrupt:
  print("Program aborted")

except Exception as error:
  print("Error or exception occurred, aborting program", error)
  traceback.print_exc()
  
finally:
  # Clean exit
  GPIO.cleanup() 
  os.system('/usr/bin/linphonecsh exit')