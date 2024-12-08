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

## First Prototype Fit
After the handset worked without any problems, I looked at how the most important components could fit into the case.
<br/>
![Pi Zero and the USB sound card in the housing of the FeTAp](/img/First%20Prototype%20Fit%20small.jpg)
<br/>

## DIY Hook Switch Circuit
I built a small circuit on a 5 x 7 cm perfboard to integrate the hook switch. I carefully desoldered the switch from the phone's original circuit board. The circuit was designed to simplify connecting the switch to a Raspberry Pi Zero. A 10 kΩ resistor was added to ensure clean signal transitions for accurate readings on the Raspberry Pi. The switch directs the supplied 3.3 volts to one of two GPIO pins, depending on whether the handset is on or off the cradle.
<br/>
### Hook Switch Circuit
![DIY Hook Switch Circuit to simplify connecting the switch to a Raspberry Pi Zero](/doc/Hoock%20Switch%20Layout%20small.png)
<br/>
<br/>
### Completed Perfboard Circuit - Bottom View
I had to route a trace around a hole with some clearance to ensure the board lies flat in the enclosure later.
![Completed Perfboard Circuit - Bottom View](/img/Hook%20bottom%20small.jpg)
<br/>
<br/>
### Completed Perfboard Circuit - Top View
![Completed Perfboard Circuit - Top View](/img/Hook%20top%20small.jpg)
<br/>

## Bell Ringer
A step-up converter, as some had suggested to ring the bell, only produced a faint clicking sound for me, rather than a proper ringing—but thankfully, A. Lang has already implemented a great solution using an ATTiny25 to generate a 25 Hertz alternating voltage and make the bell ring for one second every 4 seconds.

The forum post by A. Lang can be found here: https://www.mikrocontroller.net/topic/77664

I laid out and built the circuit from A. Lang on a 3x7cm perfboard so that it still fits in the phone.

### Bell Ringer Circuit
![DIY Bell Ringer Circuit to to control the bell with the Raspberry  Pi Zero and only 3.3 V](bell%20ringer/Bell%20Ringer%20Layout%20small.png)
<br/>
#### Parts List
* C1 100µ/16V electrolytic capacitor
* C2 10µ/63V electrolytic capacitor
* C3 4,7µ/100V electrolytic capacitor
* C4 100nF ceramic capacitor (KERKO)
* R1 1k &#8486;
* R2 56k &#8486;
* R3 10k &#8486;
* R4 10k &#8486;
* R5 56k &#8486;
* R6 56k &#8486;
* R7 1k &#8486;
* R8 56k &#8486;
* R9 1k &#8486;
* T1, T2, T3 BC547B NPN bipolar junction transistor
* T4, T5 BC557B PNP bipolar junction transistor
* T6 BS170 MOSFET (MOS field effect transistor)
* L1 470µH plugable inductors
* D1 Schottky diode (1N 5819)
* ATtiny 25
* IC socket, 8-pin
* Perforated board 30 x 70 mm
* Some copper wire 0.6mm, tinned and color of your choice

### Completed Perfboard Bell Ringer Circuit - Bottom View
At one point I had to use an insulated cable because it was too narrow
![Completed Perfboard Bell Ringer Circuit - Bottom View](/bell%20ringer/Bell%20Ringer%20Circuit%20back%20small.jpg)
<br/>
<br/>

### Completed Perfboard Bell Ringer Circuit - Top View
![Completed Perfboard Bell Ringer Circuit - Top View](/bell%20ringer/Bell%20Ringer%20Circuit%20small.jpg)
<br/>
<br/>