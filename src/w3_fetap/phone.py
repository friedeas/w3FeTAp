#!/usr/bin/env python3
from statemachine import StateMachine, State, Event

import logging
import time
import threading

from abc import ABC, abstractmethod

# Create logger
logger = logging.getLogger('w3FeTAp')

class PhoneHardware(ABC):
    
    def _set_phone_ref(self, phoneRef):
        self._phone = phoneRef
        pass

    @abstractmethod
    def _initialize(self):
        pass

    @abstractmethod
    def _indicate_initializing(self):
        pass

    @abstractmethod
    def _indicate_initialized(self):
        pass

    @abstractmethod
    def _check_for_incomming_call(self):
        pass

    @abstractmethod
    def _check_for_active_call(self):
        pass

    @abstractmethod
    def _indicate_incoming_call(self, indicate):
        pass

    @abstractmethod
    def _answer_incoming_call(self):
        pass

    @abstractmethod
    def _call_number(self):
        pass

    @abstractmethod
    def _terminate_call(self):
        pass

    @abstractmethod
    def _start_indicate_ready_to_dail(self):
        pass

    @abstractmethod
    def _stop_indicate_ready_to_dail(self):
        pass

    @abstractmethod
    def _process_dailed_number(self):
        pass

    @abstractmethod
    def _get_dail_watchdog_thread(self):
        pass

class RotaryDialTelephone(StateMachine):

    def __init__(self, hw=PhoneHardware):
        hw._set_phone_ref(self)
        self.hardWare = hw
        self._current_task = None
        super().__init__()
        

    "A sate machine for a rotary dial telephone"    
    initializing = State(initial=True)
    dysfunctional = State()
    initialized = State()
    idl = State()
    ready_to_dial = State()    
    dialing = State()
    number_dialed = State()
    called = State()
    call_number = State()
    connected = State()
    busy = State()
    ringing = State()
    terminated = State(final=True)

    _dialTone = None

    #Speed Dial Dictionary
    # 1 = **610 = Intern, up to 10 can be added
    _speedDialDictionary = {'1': '**610'}

    initComplete = (
        initializing.to(initialized)        
    )

    initFailed = (
        initializing.to(dysfunctional)
    )

    dysfunctional.to(terminated)

    done = (
        initialized.to(idl)
    )

    receiverIsPickedUp = (
        idl.to(ready_to_dial)
        | called.to(connected)
    )

    hungUp = (
        ready_to_dial.to(idl)
        | connected.to(idl)
        | busy.to(idl)
        | dialing.to(idl)
        | number_dialed.to(idl)
        | call_number.to(idl)
    )

    callComesIn = (
        idl.to(called)
    )

    callIgnored = (
        called.to(idl)
        | ringing.to(idl)
    )

    dialStoppedTurning = (
        dialing.to(number_dialed)
    )

    dialStartedTurning = (
        ready_to_dial.to(dialing)
        | number_dialed.to(dialing)
    )

    dialDelayExpired = (
        number_dialed.to(call_number)
    )

    otherPartyIsBusy = (
        call_number.to(busy)
    )

    isRinging = (
        call_number.to(ringing)
    )

    callAccepted = (
        ringing.to(connected)
    )

    shut_down = (
        initializing.to(terminated)
        | initialized.to(terminated)
        | idl.to(terminated)
        | ready_to_dial.to(terminated)
        | dialing.to(terminated)
        | number_dialed.to(terminated)
        | called.to(terminated)
        | call_number.to(terminated)
        | connected.to(terminated)        
    )

    def on_transition(self, event_data, event: Event):
        logger.info("Transition event, cancle current task")
        self._cancel_task()

    def _do_sleep(self):
        time.sleep(0.01)

    def shutdown(self):
        self._cancel_task()

    def on_enter_initializing(self):
        logger.info(self.current_state.name + " state")
        self.hardWare._indicate_initializing()
        self.hardWare._initialize()         
    
    def on_enter_initialized(self):
        logger.info(self.current_state.name + " state")
        self.hardWare._indicate_initialized()
        self.done()

    def on_enter_idl(self):
        logger.info(self.current_state.name + " state")        
        if(self.hardWare._check_for_active_call()):
            self.hardWare._terminate_call()
        logger.info("Switching to Idl task")
        self._switchTask(func=self._idlTask)

    def _idlTask(self):
        t = threading.current_thread()
        logger.info("Start idl task")
        while(self._is_not_canceled(t) and self.idl.is_active):
            if(self.hardWare._check_for_incomming_call()):
                logger.debug("Incomming call, switching state")
                self._cancel_task()
                self.callComesIn()
            self._do_sleep()
        logger.info("Idl task completed")

    def _calledTask(self):
        t = threading.current_thread()
        logger.info("Start called task")
        while(self._is_not_canceled(t) and self.called.is_active):
            if(self.hardWare._check_for_incomming_call()):
                #logger.debug("Incomming call, ring the bell")
                self.hardWare._indicate_incoming_call(True)
                self._do_sleep()
            else:                
                self.callIgnored()
        self.hardWare._indicate_incoming_call(True)
        logger.info("Called task completed")

    def _waitTask(self):
        t = threading.current_thread()
        logger.debug("Start wait task")
        while(self._is_not_canceled(t)):
            time.sleep(1)
        logger.info("wait task completed")

    def _watchdogTask(self):
        t = threading.current_thread()
        self.hardWare._get_dail_watchdog_thread().join()
        self.dialDelayExpired()

    def on_enter_ready_to_dial(self):
        logger.info(self.current_state.name + " state")
        self.hardWare._start_indicate_ready_to_dail()
        logger.info("Switching to wait task")
        self._switchTask(func=self._waitTask)

    def on_exit_ready_to_dial(self):
        logger.debug("On exit ready_to_dial state")
        self.hardWare._stop_indicate_ready_to_dail()

    def on_enter_dialing(self):
        logger.info(self.current_state.name + " state")

    def on_enter_number_dialed(self):
        logger.info(self.current_state.name + " state")
        self.hardWare._process_dailed_number()
        self._switchTask(func=self._watchdogTask)

    def on_enter_call_number(self):
        logger.info(self.current_state.name + " state")
        self.hardWare._call_number()

    def _is_not_canceled(self, t):
        return not getattr(t, "task_canceled", False)        

    def on_enter_called(self):
        logger.info(self.current_state.name + " state")
        self._switchTask(func=self._calledTask)

    def on_enter_connected(self):
        logger.info(self.current_state.name + " state")
        if(self.hardWare._check_for_incomming_call()):
            self.hardWare._answer_incoming_call()

    def on_exit_called(self):
        logger.debug("On exit called")
        self.hardWare._indicate_incoming_call(False)        

    def _switchTask(self, func):
        self._cancel_task()
        self._current_task = threading.Thread(target=func)        
        logger.info("Start new task thread")
        self._current_task.start()

    def _cancel_task(self):
        if(self._current_task is not None):
            self._current_task.task_canceled = True
            self._current_task = None