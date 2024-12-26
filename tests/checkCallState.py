#!/usr/bin/env python3
import subprocess
import os
import traceback

try:

    def _do_get_calls():
        print("before linphonecsh generic calls")
        result = subprocess.run(['linphonecsh', "generic", "calls"], capture_output = True, text = True)
        print("after linphonecsh generic calls")
        return result.stdout
    
    def _check_for_active_call():
        callStatus = _do_get_calls()
        print("Check for active calls: " +callStatus)
        if("No active call." in callStatus):
            return False
        else:
            return True

    def _check_for_incomming_call():
        callStatus = _do_get_calls()
        print("Check for incomming calls: " + callStatus)
        if("IncomingReceived" in callStatus):
            print("Return true for check for incomming calls")
            return True
        else:
            print("Return false for check for incomming calls")
            return False

    print("Init linphonecsh")
    result = subprocess.run(['./initPhone.sh'], capture_output = True, text = True)
    print(result.stdout)        
    print("before linphonecsh incomming calls")
    callStatus = _check_for_incomming_call()
    print("State: " + str(callStatus))

    print("before linphonecsh active calls")
    callStatus = _check_for_active_call()
    print("State: " + str(callStatus))
except Exception as error:
    print("Error or exception occurred, aborting program", error)
    print(traceback.format_exc())
  
finally:
    # Clean exit    
    print("Exit linphonecsh")
    os.system('/usr/bin/linphonecsh exit')