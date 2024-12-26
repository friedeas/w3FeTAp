#!/usr/bin/env python3
import subprocess
import logging
import warnings
import threading
import time
import os
import http.client as httplib
from w3_fetap.tones import DialTone
from w3_fetap.util import Watchdog
from w3_fetap.phone import PhoneHardware, RotaryDialTelephone

try:
    import RPi.GPIO as GPIO
except ImportError:
    warnings.warn('Failed to import RPi.GPIO, this should only happen during tests', ImportWarning)

# Create logger
logger = logging.getLogger('w3FeTAp')

class PiZeroFeTAp791_1(PhoneHardware):    
    # Hook Pins
    _hookIn1 = 23 # Broadcom pin 23
    _hookIn2 = 24 # Broadcom pin 24
    _hookOut = 25 # Broadcom pin 25

    # Rotary Dial Pins
    _rotaryDialOutWhite = 20 # Broadcom pin 20
    _rotaryDialOutYellow = 21 # Broadcom pin 21
    _rotaryDialInGreen = 5 # Broadcom pin 5
    _rotaryDialInBrown = 6 # Broadcom pin 6

    _greenLedCtl = 22 # Broadcom pin 22
    _redLedCtl = 27 # Broadcom pin 27
    _change_delay = 1

    # Bell Ring Ctl.
    _bellRingCtl = 17 # Broadcom pin 17

    #State identified by the hook switch
    _receiverIsInTheCradle = False

    #Global variables for the rotating dial
    #rotating = False
    _pulsCount = 0

    #Global variable for the dailing state
    _dailWatchdogTimeout = 4
    #dailing = False
    _numberToDail = ""
    _watchdog = Watchdog(_dailWatchdogTimeout)

    _initThread = None    

    def _updateHookState (self, args):
        if GPIO.input(self._hookIn1):
            logger.info("HookIn 1 is high => The receiver is picked up")
            self._receiverIsInTheCradle = False
            if(RotaryDialTelephone.idl == self._phone.current_state
               or RotaryDialTelephone.called == self._phone.current_state):
                self._phone.receiverIsPickedUp()            
        if GPIO.input(self._hookIn2):
            logger.info("HookIn 2 is high => The receiver is in the cradle")
            self._receiverIsInTheCradle = True
            if(RotaryDialTelephone.ready_to_dial == self._phone.current_state 
               or RotaryDialTelephone.busy == self._phone.current_state
               or RotaryDialTelephone.connected == self._phone.current_state
               or RotaryDialTelephone.dialing == self._phone.current_state
               or RotaryDialTelephone.number_dialed == self._phone.current_state
               or RotaryDialTelephone.call_number == self._phone.current_state):
                self._phone.hungUp()
            else:
                logger.debug("Ignore unexpected hungUp in state: " + self._phone.current_state.name)
            self._watchdog.cancel()
            
    #Dial Pulse
    def _processDialPulse(self, args):        
        if GPIO.input(self._rotaryDialInGreen) == GPIO.LOW:
            logger.debug("Puls detected in sate: " + self._phone.current_state.name)
            if(RotaryDialTelephone.dialing == self._phone.current_state):
                logger.debug("Dialing state, start counting")
                self._watchdog.refresh()                
                self._pulsCount += 1

    
    #RotatingDial
    def _processRotatingDial(self, args):
        global dailing        
        
        global numberToDail
            
        if GPIO.input(self._rotaryDialInBrown):
            logger.info("Rotary dial turns")            
            #reset
            self._pulsCount = 0
            self._phone.dialStartedTurning()
        else:   
            logger.info("Dial no longer rotates")
            self._phone.dialStoppedTurning()            

    def _initialize_gpio(self):
        logger.info("Initializing GPIO ports and event listener.")                

        # Init bell ring ctl
        GPIO.setup(self._bellRingCtl, GPIO.OUT)

        # Init the rotary dial pins
        GPIO.setup(self._rotaryDialOutWhite, GPIO.OUT)
        GPIO.setup(self._rotaryDialOutYellow, GPIO.OUT)
        GPIO.setup(self._rotaryDialInGreen, GPIO.IN)
        GPIO.setup(self._rotaryDialInBrown, GPIO.IN)        
        GPIO.output(self._rotaryDialOutWhite, GPIO.HIGH)
        GPIO.output(self._rotaryDialOutYellow, GPIO.HIGH)

        # Init hook switch pins
        GPIO.setup(self._hookIn1, GPIO.IN)
        GPIO.setup(self._hookIn2, GPIO.IN)
        GPIO.setup(self._hookOut, GPIO.OUT)
        GPIO.output(self._hookOut, GPIO.HIGH)

        # Init hook switch event listener
        GPIO.add_event_detect(self._hookIn1, GPIO.BOTH, callback=lambda x:self._updateHookState(self), bouncetime=200)
        # Init rotary dial event listener
        GPIO.add_event_detect(self._rotaryDialInGreen, GPIO.FALLING, callback=lambda x:self._processDialPulse(self), bouncetime=50 )
        GPIO.add_event_detect(self._rotaryDialInBrown, GPIO.BOTH, callback=lambda x:self._processRotatingDial(self), bouncetime=50)
        
        self._updateHookState(self)

        logger.info("GPIO initializing completed")

    def _initialize_audio(self):
        logger.info("Trying initialize audio")
        self._dialTone = DialTone()
        logger.info("Audio initialized")

    def _check_network(self):
        conn = httplib.HTTPSConnection("8.8.8.8", timeout=5)
        try:
            conn.request("HEAD", "/")            
            logger.info("Network reachable")
            return True
        except Exception:            
            logger.info("Network not reachable!")
            return False
        finally:
            conn.close()

    def _initialize_linphone(self):
        logger.info("Trying initialize linphonecsh")
        result = subprocess.run(['./initPhone.sh'], capture_output = True, text = True)
        logger.info(result.stdout)
        logger.info("Linphone initialized")

    def _check_linphone_state(self):
        logger.info("Verifying linphonecsh state")
        #linphonecsh soundcard show
        logger.info("Linphone soundcard state")
        soundcars_state = subprocess.run(['linphonecsh', "soundcard", "show"], capture_output = True, text = True)
        logger.info(soundcars_state.stdout)
        logger.info("Linphone account state")
        sip_account_state_output = subprocess.run(['linphonecsh', "status", "register"], capture_output = True, text = True)        
        sip_account_state = sip_account_state_output.stdout
        logger.info(sip_account_state)
        if(not "registered, identity=" in sip_account_state):
            logger.info("Linphone account is not available!")
            return False
        else:
            logger.info("Linphone account successful registered")
            return True

    def _initialize(self):
        max_retries = 10        
        self._initialize_gpio()
        self._initialize_audio()
        while(not self._check_network()):
            #ToDo add max retries
            logger.info("Waiting for network")
            time.sleep(3)
        self._initialize_linphone()
        linphone_initialized = self._check_linphone_state()
        if(not linphone_initialized):
            logger.info("linphonecsh not ready, retry setting it up")
            attempts = 0
            while (attempts < max_retries and not linphone_initialized):
                time.sleep(5)
                logger.info("Retry to initialize linphonecsh")
                self._initialize_linphone()
                attempts += 1
                linphone_initialized = self._check_linphone_state()
            if(not linphone_initialized):
                logger.info("Shuting down w3FeTAp!")
                self._initThread.do_blink = False
                self._initThread.join()
                GPIO.output(self._greenLedCtl, GPIO.LOW)
                GPIO.output(self._redLedCtl, GPIO.HIGH)
                self._phone.shut_down()
            else:
                self._phone.initComplete()
        else:
            self._phone.initComplete()

    def _blinkGreen(self):
        t = threading.current_thread()        
        while getattr(t, "do_blink", True):
            GPIO.output(self._greenLedCtl, GPIO.HIGH)
            time.sleep(self._change_delay)
            GPIO.output(self._greenLedCtl, GPIO.LOW)
            time.sleep(self._change_delay)

    def _indicate_initializing(self):        
        # Init LED ctl
        GPIO.cleanup() 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._redLedCtl, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._greenLedCtl, GPIO.OUT, initial=GPIO.LOW)
        logger.info("Show initializing")
        self._initThread = threading.Thread(target=self._blinkGreen)
        self._initThread.start()

    def _indicate_initialized(self):
        logger.info("Show initialized")        
        self._initThread.do_blink = False
        self._initThread.join()
        GPIO.output(self._greenLedCtl, GPIO.HIGH)

    def _do_get_calls(self):
        #logger.debug("before linphonecsh generic calls")
        result = subprocess.run(['linphonecsh', "generic", "calls"], capture_output = True, text = True)
        #logger.debug("after linphonecsh generic calls")
        return result.stdout

    def _check_for_incomming_call(self):
        callStatus = self._do_get_calls()
        #logger.debug("Check for incomming calls: " + callStatus)
        if("IncomingReceived" in callStatus):
            #logger.debug("Return true for check for incomming calls")
            return True
        else:
            #logger.debug("Return false for check for incomming calls")
            return False
        
    def _check_for_active_call(self):
        callStatus = self._do_get_calls()
        logger.debug("Check for active calls: " +callStatus)
        if("StreamsRunning" in callStatus or "OutgoingEarlyMedia" in callStatus):
            logger.debug("Return true for check for active calls")
            return True
        else:
            logger.debug("Return false for check for active calls")
            return False            
        
    def _indicate_incoming_call(self, indicate):
        if(indicate == True):
            if(RotaryDialTelephone.called == self._phone.current_state):
                if(GPIO.input(self._bellRingCtl)):
                    logger.debug("Indicating incoming call")
                    GPIO.output(self._bellRingCtl, GPIO.LOW)
            else:
                logger.debug("Ignore _indicate_incoming_call called from unexpected state! " + self._phone.current_state.name)
        else:            
            logger.debug("Stop indicating incoming call")
            GPIO.output(self._bellRingCtl, GPIO.HIGH)

    def _answer_incoming_call(self):
        logger.debug("Answer incomming call: ")
        os.system("linphonecsh generic \"answer $(linphonecsh generic 'calls' | sed -n 4p | awk '{print $1}')\"")
        
    def _start_indicate_ready_to_dail(self):
        #reset previous dialed number
        self._numberToDail = ""
        logger.info("Start indicate ready to dail")
        self._dialTone.play()
        
    def _stop_indicate_ready_to_dail(self):
        logger.info("Stop indicate ready to dail")
        self._dialTone.stop()

    def _process_dailed_number(self):
        logger.debug("Get dailed number")        
        numberString = str(self._pulsCount)
        logger.info("Number of pulses: " + numberString + "\n")
        if('10' == numberString):
            numberString = '0'
        if(len(self._numberToDail) == 0):
            self._watchdog.start()
            logger.debug("Start dail timeout watchdog")
        self._numberToDail = self._numberToDail + numberString    
    
    def _get_dail_watchdog_thread(self):
        return self._watchdog._t
    
    def _call_number(self):
        phoneNumber = self._numberToDail
        if(len(phoneNumber) > 0):
            if(len(phoneNumber) == 1):
                speedDialNumber = self._phone._speedDialDictionary.get(phoneNumber)              
                if(speedDialNumber is not None):
                    logger.info("Speed dial number " + speedDialNumber + " for " + phoneNumber)
                    phoneNumber = speedDialNumber
            logger.info("Dailing phone number: " + phoneNumber)            
            os.system('linphonecsh dial ' + phoneNumber)

    def _terminate_call(self):
        os.system('linphonecsh generic terminate')