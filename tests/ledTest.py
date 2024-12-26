#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

green_ld_ctl = 22 # Broadcom pin 22
red_led_ctl = 27 # Broadcom pin 27
change_delay = 2

try:  
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(red_led_ctl, GPIO.OUT, initial=GPIO.LOW)
  GPIO.setup(green_ld_ctl, GPIO.OUT, initial=GPIO.LOW)

  def blink():
    print("Red control low")
    GPIO.output(red_led_ctl, GPIO.LOW)    
    print("Green control high")
    GPIO.output(green_ld_ctl, GPIO.HIGH)
    time.sleep(change_delay)
    print("\nchanging color\n")
    print("Red control high")
    GPIO.output(red_led_ctl, GPIO.HIGH)
    print("Green control low")
    GPIO.output(green_ld_ctl, GPIO.LOW)
    time.sleep(change_delay)
    print("\nchanging color\n")

  while True:
    blink()
  
except KeyboardInterrupt:      
    print("Program aborted")
  
except Exception as error:
    print("Error or exception occurred, aborting program", error)  
  
finally:  
    GPIO.cleanup() # this ensures a clean exit  