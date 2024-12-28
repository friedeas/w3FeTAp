# w3FeTAp Project Documentation
## A fun purchase got the project started
It was actually just a joke and I didn't think I would win the auction with that bid.
<br/>
![Picture of the green rotary dial phone FeTap 791-1, auctioned on eBay](/img/Ebay_small.png)
<br/>
The phone was in very good condition for its age and it was too good to just leave it sitting around.

## Testing the SW & HW Setup
Connecting a headset with the USB sound card and test if everyting is working well. If so, it should look like this:
<br/>
![Screenshot of the test to initiate Linphone and registering a SIP account](/img/Bash%20Test.png)
<br/>

## Test with the handset
Next I tested whether it also works with the telephone handset. 
<br/>
![Telephone handset test wiring with 3.5 jack plugs](/img/Handset%20Test%20Wiring%20small.jpg)
<br/>
Surprisingly, it worked right away without any major problems.
## First Prototype Fit
After the handset worked without any problems, I looked at how the most important components could fit into the case.
<br/>
![Pi Zero and the USB sound card in the housing of the FeTAp](/img/First%20Prototype%20Fit%20small.jpg)
<br/>

## DIY Hook Switch Circuit
I carefully desoldered the switch from the phone's original circuit board and embedded it in a small circuit on a 5 x 7 cm perfboard.</br>
![Completed Perfboard Circuit - Top View](/img/Hook%20top%20small.jpg)
</br>
Later I extended the circuit a bit and added pull-down resistors for the two different signal lines of the rotary dial.

## Bell Ringer
A step-up converter, as some had suggested to ring the bell, only produced a faint clicking sound for me, rather than a proper ringing—but thankfully, A. Lang has already implemented a great solution using an ATTiny25 to generate a 25 Hertz alternating voltage and make the bell ring for one second every 4 seconds.

The forum post by A. Lang can be found here: https://www.mikrocontroller.net/topic/77664
</br>
</br>
![Circuit diagram by A. Lang](/bell%20ringer/bimmel.png)
</br>
</br>
I first built and tested the circuit on a breadboard.
</br>
![Breadboard test setup of the bell circuit](/doc/Breadboard%20test%20circuit.jpg)
</br>
After successful testing, I designed a compact circuit that also fits well into the phone. I used [DIY Layout Creator](https://github.com/bancika/diy-layout-creator) to [design](/bell%20ringer/Bell%20Ringer%20Layout.diy) and built the circuit from A. Lang on a 30 x 70 mm perfboard.
</br>
![Completed Perfboard Bell Ringer Circuit - Top View](/bell%20ringer/Bell%20Ringer%20Circuit%20small.jpg)
</br>
</br>
This was a nice and solvable soldering exercise, which eventually led to success, not without some troubleshooting.
</br>
</br>
![Completed Perfboard Bell Ringer Circuit - Bottom View](/bell%20ringer/Bell%20Ringer%20Circuit%20back%20small.jpg)

## Duo-LED control circuit
I wanted to equip one of the cable openings, which is no longer used, with an LED to display the status of the phone. Flashing green for the start-up phase, steady green when the phone is ready and red if something has gone wrong.
</br>
</br>
![Duo-LED control circuit](/doc/LED%20Ctl%20small.png)

## The final result with all parts assembled
After several iterations and a few failures, the end result looked okay.
</br>
</br>
![w3FeTAp assembled with all custom circuits](/doc/Complete%20phone%20with%20all%20created%20circuits.jpg)

## Software for the authentic 80s phone
The phone should feel and sound as much as possible like the phone from my childhood memories. The first disappointment, or challenge, was that VoIP phones do not use an acoustic signal to indicate to the user that a call can be made. This behavior of playing the so-called dial tone when picking up the handset had to be reproduced. Luckily I found this continuous tone here: https://de.wikipedia.org/wiki/Datei:1TR110-1_Kap8.1_Waehlton.ogg licenced under the Creative Commons. (see [README.md](/audio/README.md) for more details)

For the implementation I used the python statemachine, which created this nice diagram via Graphviz.
</br>
</br>
![w3FeTAp Rotary Dial Telephone State Machine](/doc/RotaryDialTelephoneStateMachine.png)
</br>
</br>
The final challenge was to realize the automatic start of the software. Normally I would choose the systemd route for this task, which in this case turned out to be quite complicated. In addition to Linphone, the software also requires an initialized PulseAudio stack, therefore the way via a start script in the .bashrc proved to be much easier. The only challenge that still needed to be solved was to build a waiting loop for the network availability into the software.

## Conclusion
In addition to some Python, I also learned a little about electronics, capacitors and circuits in general. However, the following points surprised me.
* This telephone from the 80s could easily be disassembled down to the smallest part and was still in very good condition after all this time.
* It is somewhat shocking how little of it remains today when you compare it to current consumer electronics
* My children had to learn how to use the rotary dial and that you have to pick up the receiver before dialing
* Even the simple and relatively straightforward technique cannot be used without explanation if the context of experience is completely different