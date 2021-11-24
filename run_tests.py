#!/usr/bin/env micropython

import unittest
import sys
import machine


sys.path.append("src")


def mock_pin__init__(self, id, dir="in"):
    self.id = id
    self.mock_value = None
    self.dir = dir


def mock_pin_init(self, dir="in", pull=None):
    self.mock_value = None
    self.dir = dir
    self.pull = pull


def mock_pin_value(self, v=None):
    print("mocking value ", v)
    if v is None:
        return 1 if self.mock_value == b"1" else 0
    self.mock_value = (b"1" if v else b"0")


machine.Pin.__init__ = mock_pin__init__
machine.Pin.init = mock_pin_init
machine.Pin.value = mock_pin_value


unittest.main("tests")
