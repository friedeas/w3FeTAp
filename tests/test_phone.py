#!/usr/bin/env python3
import logging
import logging.config
from w3_fetap.phone import RotaryDialTelephone
from tests.mocks import TestPhoneHardware

logging.config.fileConfig('logging.conf')

def test_IdleState():
    phone = RotaryDialTelephone(hw=TestPhoneHardware())
    print("State: " + phone.current_state.name )
    assert RotaryDialTelephone.idl == phone.current_state
    phone.shutdown()

def test_IdleState():
    phone = RotaryDialTelephone(hw=TestPhoneHardware())
    print("State: " + phone.current_state.name )
    assert RotaryDialTelephone.idl == phone.current_state
    phone.receiverIsPickedUp()
    assert RotaryDialTelephone.ready_to_dial == phone.current_state
    phone.shutdown()