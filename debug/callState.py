#!/usr/bin/env python3
import subprocess

testOutput = """Call states
Id |            Destination              |      State      |    Flags   |
------------------------------------------------------------------------
1  | "Xxxxxxx 1" <sip:**610@fritz.box>   | IncomingReceived |
"""

testOutput2 = """Call states
Id |            Destination              |      State      |    Flags   |
------------------------------------------------------------------------
1  | sip:010101010101@fritz.box          | IncomingReceived |
"""

RINGCHECK = 'echo -e "' + testOutput + '" | sed -n 4p | awk \'{print $7}\''
RINGVALUE = subprocess.check_output(['bash', '-c', RINGCHECK ]).decode().strip()
print("RINGVALUE: " + RINGVALUE)

print("Using Grep on output 1")
found = False
RINGCHECK = 'echo -e "' + testOutput + '" | sed -n 4p'
line4 = subprocess.check_output(['bash', '-c', RINGCHECK ]).decode().strip()
print("sed result: " + line4)
found = "IncomingReceived" in line4;
print("IncomingReceived found in line 4: " + str(found))

found = False
print("Using Grep on output 2")
RINGCHECK = 'echo -e "' + testOutput2 + '" | sed -n 4p'
line4 = subprocess.check_output(['bash', '-c', RINGCHECK ]).decode().strip()
print("sed result: " + line4)
found = "IncomingReceived" in line4;
print("IncomingReceived found in line 4: " + str(found))