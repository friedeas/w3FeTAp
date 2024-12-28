# Overview of the circuits used
To control the bell ringer, read the state of the hook switch, the pulses of the rotary dial and control the Duo-LED I used the following circuits.

## Bell Ringer Circuit
The circuit includes an 8-bit AVR microcontroller ATTiny25 to generate a 25 Hz alternating voltage and make the bell ring every 4 seconds, if the control line is pulled to GND.

Details and license information are documented in this [README.md](/bell%20ringer/README.md)

![DIY Bell Ringer Circuit to to control the bell with the Raspberry  Pi Zero and only 3.3 V](/bell%20ringer/Bell%20Ringer%20Layout%20small.png)
<br/>
### Parts List
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
* L1 470µH plugable inductor
* D1 Schottky diode (1N 5819)
* ATtiny 25
* IC socket, 8-pin
* Perforated board 30 x 70 mm
* Some copper wire 0.6mm, tinned and color of your choice

You will need an Arduino Uno, or something like a USBASP AVR Programmer to flash the ATtiny25. Wolfgang Ewald has written an excellent guide in German for this: https://wolles-elektronikkiste.de/attiny-mit-arduino-code-programmieren. This guide is also available in English: https://wolles-elektronikkiste.de/en/programming-attiny-with-arduino-code

### Completed Perfboard Bell Ringer Circuit - Bottom View
At one point I had to use an insulated cable because it was too narrow
![Completed Perfboard Bell Ringer Circuit - Bottom View](/bell%20ringer/Bell%20Ringer%20Circuit%20back%20small.jpg)
<br/>
<br/>

### Completed Perfboard Bell Ringer Circuit - Top View
![Completed Perfboard Bell Ringer Circuit - Top View](/bell%20ringer/Bell%20Ringer%20Circuit%20small.jpg)
<br/>
<br/>

## Hook Switch Circuit
I built a small circuit on a 5 x 7 cm perfboard to integrate the hook switch and two of the four dial cables. The other two are each connected directly to a GPIO pin. I carefully desoldered the switch from the phone's original circuit board. The circuit was designed to simplify connecting the switch to a Raspberry Pi Zero. Four 10 kΩ pull-down resistor were added to ensure clean signal transitions for accurate readings on the Raspberry Pi. The switch directs the supplied 3.3 volts via GPIO out to one of two GPIO pins 23 or 24, depending on whether the handset is on or off the cradle.

![DIY Hook Switch Circuit to simplify connecting the switch to a Raspberry Pi Zero](/doc/Hoock%20Switch%20Layout%20small.png)
<br/>
<br/>
### Completed Hook Switch Perfboard Circuit - Bottom View
I had to route a trace around a hole with some clearance to ensure the board lies flat in the enclosure later. The picture shows a previous version that did not yet include a proper pull-down resistors and the connections for the dial are also missing.
![Completed Perfboard Circuit - Bottom View](/img/Hook%20bottom%20small.jpg)
<br/>
<br/>
### Completed Hook Switch Perfboard Circuit - Top View
![Completed Perfboard Circuit - Top View](/img/Hook%20top%20small.jpg)
<br/>
<br/>
## Duo-LED control circuit
The GPIO outputs of the Raspberry PI do not provide enough current for the Duo-LED. Therefore, I built this small circuit that uses the 5 volt power supply and is controlled via two NPN BC547 transistors. With two 1 k&#8486; resistors and the appropriate LED resistors, the circuit is complete.
![Duo-LED control circuit](/doc/LED%20Ctl%20small.png)
<br/>
<br/>