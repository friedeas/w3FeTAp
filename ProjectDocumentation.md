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