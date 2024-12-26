#!/usr/bin/env python3
import logging
from w3_fetap.phone import PhoneHardware

# Create logger
logger = logging.getLogger('w3FeTAp')

class TestPhoneHardware(PhoneHardware):

    def __init__(self):
        self._mock_called = False

    def _initialize(self):
        print("Initializing TestPhoneHardware")

    def _ceckForCalls(self):
        return self._mock_called
    
    def _start_indicate_ready_to_dail(self):
        print("Start playing ready to dail audio")   
    
    def _indicate_initializing(self):
        pass

    def _indicate_initialized(self):
        pass

    def _check_for_incomming_call(self):
        pass

    def _check_for_active_call(self):
        pass

    def _indicate_incoming_call(self, indicate):
        pass

    def _answer_incoming_call(self):
        pass

    def _call_number(self):
        pass

    def _terminate_call(self):
        pass

    def _start_indicate_ready_to_dail(self):
        pass

    def _stop_indicate_ready_to_dail(self):
        pass

    def _process_dailed_number(self):
        pass

    def _get_dail_watchdog_thread(self):
        pass