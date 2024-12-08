# w3FeTAp
Converting a Fernsprechtischapparat (FeTap) 791-1 into a VoIP phone utilizing a Pi Zero W, Linphone and some Python code. And so an old-fashioned device from the 80s becomes a top modern World Wide Web Telephone Table Device, or in short w3FeTAp.

## Seriously?
Actually, I just wanted to show my kids that phones didn't always look like this. I got the FeTap 791-1 cheaply on eBay and didn't want to let it just sit around uselessly. Fortunately, I came across these two websites, which made it easy for me to get started.
* [FeTaPi](https://git.kasiandras-dreams.de/Kasiandra/fetapi)
* [VoIP-FeTAp](https://wiki.lugsaar.de/projekte/ip-fetap)

## Which parts did I use
* FeTap 791-1
* Raspberry Pi Zero W v.1.1
* USB sound card (I used the LogiLink UA0078)
* USB to micro USB adapter
* A few small parts like jack plugs and cables
* [ATTiny25 based circuit](bell%20ringer/README.md) to generate 25 Hertz alternating voltage to rin the bell (buck–boost converter solution didn't work well enough for me)

## Preparing and testing the system
1. Follow the instruction here: https://github.com/raspberrypi/rpi-imager to install the Raspberry Pi Imager for your operating system
2. Select your Raspberry Pi version and the OS (I selected Bookworm based Pi OS)
3. Use the OS customisation menu to
    * Configure the Wi-Fi credentials
    * Your keyboard layout
    * Enable SSH in the services tab
4. Start the Pi Zero and install the required packages
    ```Shell
    $ sudo apt install linphone-nogtk pulseaudio doxygen python3-pip python3-RPi.GPIO python3-pystache python3-six
    ```
5. Poweroff the Pi Zero (to prevent an unwanted restart bacause of the inrush current problem)
    ```Shell
    $ sudo poweroff
    ```
    * Connect the USB sound card via the micro USB adapter
7. Set PulseAudio as the audio configuration
    ```Shell
    $ sudo raspi-config
    ```
    * Advanced Options ->  Audio Config -> PulseAudio
8. Test the audio setup
    * Connect a headphone and an microphone with the USB sound card
    * Check the output
        ```Shell
        $ speaker-test -t wav
        ```
    * Try to record a short test sequence
        ```Shell
        $ arecord -d 5 -f cd test.wav 
        ```
    * Check the recording
        ```Shell
        $ aplay test.wav
        ```
        <br>

    > [!TIP]
    > In case of issues try to solve them. This page could be helpful https://wiki.archlinux.org/title/PulseAudio Troubleshooting#Microphone_not_detected_by_PulseAudio

    <br>
9. Configure an IP phone account
    * Use an Fritzbox to configure an IP phone (german documentation) https://blog.hommel-net.de/archives/556-Telefonieren-unter-Linux-mit-Linphone-und-der-Fritzbox.html
    * Use any other VoIP provider account
10. Make a test call
    * Prepare Linphone
        ```Shell
        $ linphonecsh init
        $ linphonecsh soundcard playback
        $ linphonecsh soundcard ring
        $ linphonecsh register --username YOUR_USER_NAME --host 192.168.178.1 --password YOUR_PASSWORD
        ```
        <br>

        > [!TIP]
        > Make sure to use the username and password of your IP phone account
        > Replace the IP 192.168.178.1 with the IP of your Fritzbox or server name of your VoIP provider

        <br>

    * Initiate an outbound SIP call
        ```Shell
        $ linphonecsh dial 'sip:**610@192.168.178.1'
        ```
        <br>

        > [!TIP]
        > **610 is the internal number of a phone regisered as a IP phone on a Fritzbox.
        > Replace replace this with your target phone number or matching internal number

        <br>

        > [!NOTE]
        > Apparently the prefix sip: and the @hostname part was or is not necessary, but it already led to the error message "Error from linphone_core_invite" for me dialing without the prefix. 

## Third-Party Software
The folder "[bell ringer](bell%20ringer/)" contains code from the project [Telefonklingel mit Tiny25 ansteuern](https://www.mikrocontroller.net/topic/77664) under the [GNU General Public License, Version 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html.en). 