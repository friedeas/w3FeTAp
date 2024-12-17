#!/bin/bash

# Ensure to create a sip.config containing username, host and password as key values
. sip.config
echo 'Trying to shut down linphonecsh'
/usr/bin/linphonecsh exit
sleep 5
echo 'Initializing linphonecsh'
/usr/bin/linphonecsh init
sleep 10
echo 'linphonecsh initialized'
echo 'Configuring playback'
/usr/bin/linphonecsh soundcard playback
echo 'Soundcard playback configured'
sleep 1
echo 'Configuring ring'
/usr/bin/linphonecsh soundcard ring
echo 'Soundcard ring configured'
sleep 1
echo 'Registering SIP account'
/usr/bin/linphonecsh register --username $username --host $host --password $password
echo 'User account registered'
sleep 1
