# w3FeTAp
Converting a Fernsprechtischapparat (FeTap) 791-1 into a VoIP phone utilizing a Pi Zero W, Linphone and some Python code. And so an old-fashioned device from the 80s becomes a top modern World Wide Web Telephone Table Device, or in short w3FeTAp.

In the [project documentation](ProjectDocumentation.md) I show the individual steps of the assembly process.

## Seriously?
Actually, I just wanted to show my kids that phones didn't always look like this. I got the FeTap 791-1 cheaply on eBay and didn't want to let it just sit around uselessly. Fortunately, I came across these two websites, which made it easy for me to get started.
* [FeTaPi](https://git.kasiandras-dreams.de/Kasiandra/fetapi)
* [VoIP-FeTAp](https://wiki.lugsaar.de/projekte/ip-fetap)

## Which parts did I use
* [FeTap 791-1](https://de.wikipedia.org/wiki/Fernsprechtischapparat#FeTAp_79)
* Raspberry Pi Zero W v.1.1
* USB sound card (I used the LogiLink UA0078)
* USB to micro USB adapter
* [ATTiny25 based circuit](/doc/Circuits.md#bell-ringer-circuit) to generate 25 Hertz alternating voltage to rin the bell (buck–boost converter solution didn't work well enough for me)
* A simple, self-designed [perfboard for the hook switch](/doc/Circuits.md#hook-switch-circuit) and to be able to read the pulses of the dial cleanly
* A small strip grid board for the [Duo-LED control](/doc/Circuits.md#duo-led-control-circuit)
* A few small parts like hexagon nylon spacers, jack plugs and cables
* Superglue and baking soda

## Preparing and testing the system
1. Follow the instruction here: https://github.com/raspberrypi/rpi-imager to install the Raspberry Pi Imager for your operating system
2. Select your Raspberry Pi version and the OS (I selected Bookworm based Pi OS)
3. Use the OS customisation menu to
    * Configure the Wi-Fi credentials
    * Your keyboard layout
    * Enable SSH in the services tab
4. Start the Pi Zero and install the required packages
    ```Shell
    $ sudo apt install linphone-nogtk pulseaudio doxygen python3-pip python3-rpi-lgpio python3-pystache python3-six
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
11. Setup Python and install the project
    * Change to the home directory
    ```Shell
    $ cd ~
    ```    
    * Clone the w3FeTAp project repository
    ```Shell
    $ git clone https://github.com/friedeas/w3FeTAp
    ```
    * Create a virtual Python environment in this folder (allow usage of system packages and name it pyenv)
    ```Shell
    $ python3 -m venv --system-site-packages --prompt pyenv ~/w3FeTAp/pyenv
    ```
    * Change to the w3FeTAp directory
    ```Shell
    $ cd w3FeTAp
    ```
    * Install w3FeTAp via pip (the -e switch is optional but would allow you to edit the Python files)
    ```Shell
    $ pip install -e .
    ```
12. Start the w3FeTAp app manually
    * Configure your SIP account
    The sip.config file nned to contain the following variables</br>
    username=</br>
    host=</br>
    password=</br>
    ```Shell
    $ nano ~/w3FeTAp/sip.config
    ```    
    * Start the app manually
    ```Shell
    $ python -m w3_fetap.w3_fetap_app
    ```
    * If everything worked well, the green LED should flash briefly and then remain permanently green and no error messages should appear in the console.
    * If you encounter issues try to use the Python scripts in the tests folder to solve them
13. Automate the start if you wish
    * Use .bashrc to automatically start w3FeTAp
    ```Shell
    $ nano .bashrc
    ```
    * Add the following line as the last entry in this file. The flock command ensures that w3FeTAp is only launched once.
    ```Shell
    flock -n ~/w3FeTAp/w3lockfile ~/w3FeTAp/w3fetap-service.sh &
    ```
    

## Third-Party Software
The folder "[bell ringer](bell%20ringer/)" contains code from the project [Telefonklingel mit Tiny25 ansteuern](https://www.mikrocontroller.net/topic/77664) under the [GNU General Public License, Version 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html.en).

The folder [audio](audio/) containse the file 1TR110-1_Kap8.1_Waehlton.ogg, created by arvedkrynil, that is licensed under the Creative Commons Attribution-ShareAlike [3.0 Unported](https://creativecommons.org/licenses/by-sa/3.0/), [2.5 Generic](https://creativecommons.org/licenses/by-sa/2.5/), [2.0 Generic](https://creativecommons.org/licenses/by-sa/2.0/) and [1.0 Generic](https://creativecommons.org/licenses/by-sa/1.0/). Source https://de.wikipedia.org/wiki/Datei:1TR110-1_Kap8.1_Waehlton.ogg