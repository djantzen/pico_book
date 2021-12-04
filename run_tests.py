#!/usr/bin/env micropython

import unittest
import sys
import machine


sys.path.append("src")


def mock_pin__init__(self, id, dir="in"):
    self.id = id
    self.mock_value = None
    self.dir = dir


class PinEvent:
    def __init__(self, old_value, new_value):
        self.old_value = old_value
        self.new_value = new_value


def mock_pin_init(self, dir="in", pull=None):
    self.mock_value = None
    self.dir = dir
    self.pull = pull
    self.events = []

# Based on machine.Pin implementation
#     def value(self, v=None):
#         if v is None:
#             self.f.seek(0)
#             return 1 if self.f.read(1) == b"1" else 0
#         self.f.write(b"1" if v else b"0")

def mock_pin_value(self, value=None):
    print("mocking value ", value)
    if value is None:
        return 1 if self.mock_value == b"1" else 0
    event = PinEvent(self.mock_value, (b"1" if value else b"0"))
    self.events.append(event)
    self.mock_value = event.new_value


machine.Pin.__init__ = mock_pin__init__
machine.Pin.init = mock_pin_init
machine.Pin.value = mock_pin_value


unittest.main("tests")
