#!/usr/bin/env python3
import logging
import threading
# Create logger
logger = logging.getLogger('w3FeTAp')

class Watchdog():
  
  def __init__(self, timeout):
    self.timeout = timeout
    self.expired = False
    self.cancelled = False
    self._t = None

  def do_expire(self):
    self.expired = True

  def _expire(self):
    logger.debug("\nWatchdog expire")
    self.do_expire()

  def start(self):
    self.cancelled = False
    if self._t is None:
      self._t = threading.Timer(self.timeout, self._expire)
      self.expired = False
      self._t.start()
    else:
      self.refresh()

  def stop(self):
    if self._t is not None:
      self._t.cancel()
      self._t = None
      self.expired = False

  def refresh(self):
    if self._t is not None:
      self.stop()
      self.start()

  def cancel(self):
    self.cancelled = True