#!/usr/bin/env python3
import logging
import logging.config
import RPi.GPIO as GPIO
import os
from os import environ
import sys
import signal
import threading
import time
import traceback
from w3_fetap.phone import RotaryDialTelephone
from w3_fetap.hardware import PiZeroFeTAp791_1

class SignalWatchdog:
  
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self, signum, frame):
    self.kill_now = True

def cleanup_on_exit():
    stop_event.set()
    print("Cleanup on exit")
    GPIO.cleanup() 
    os.system('/usr/bin/linphonecsh exit')
    sys.exit(0)

def main():    
    logger = None
    try:        
        signal_watchdog = SignalWatchdog()
        print("Try to setup logging")
        print("Try reading system environment variable W3_FETAP_LOG_CONF")
        logfileConfig = environ.get('W3_FETAP_LOG_CONF')
        if (logfileConfig is None):
            print("Set env variable W3_FETAP_LOG_CONF to profige logging configuration file!")
            sys.exit(1)
        print("Checking if logging config file can be read: " + logfileConfig)        
        if (not os.access(logfileConfig, os.R_OK)):
            print("Logging configuration file not found: " + logfileConfig)
            sys.exit(1)
        logging.config.fileConfig(str(logfileConfig))
        # Create logger
        logger = logging.getLogger('w3FeTAp')
        logger.info("Starting w3FeTAP")
        phone = RotaryDialTelephone(hw=PiZeroFeTAp791_1())
        while(phone.current_state is not RotaryDialTelephone.terminated and not signal_watchdog.kill_now):
            time.sleep(1)
        cleanup_on_exit()

    except Exception as error:
        if(logger is not None):
            logger.error("Error or exception occurred, aborting program", error)
            logger.error(traceback.format_exc())
        else:
            print("Error or exception occurred, aborting program \n" + traceback.format_exc())   
        cleanup_on_exit()       

if __name__ == "__main__":
    stop_event = threading.Event()
    main()
