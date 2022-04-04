"""
Represents the single Pico MCU.
"""

import machine
import re


class Pico:

    _instance = None

    def __init__(self):
        self._is_initialized = False

    def _initialize(self):
        self.gp0 = machine.Pin(0)
        self.gp1 = machine.Pin(1)
        self.gp2 = machine.Pin(2)
        self.gp3 = machine.Pin(3)
        self.gp4 = machine.Pin(4)
        self.gp5 = machine.Pin(5)
        self.gp6 = machine.Pin(6)
        self.gp7 = machine.Pin(7)
        self.gp8 = machine.Pin(8)
        self.gp9 = machine.Pin(9)
        self.gp10 = machine.Pin(10)
        self.gp11 = machine.Pin(11)
        self.gp12 = machine.Pin(12)
        self.gp13 = machine.Pin(13)
        self.gp14 = machine.Pin(14)
        self.gp15 = machine.Pin(15)
        self.gp16 = machine.Pin(16)
        self.gp17 = machine.Pin(17)
        self.gp18 = machine.Pin(18)
        self.gp19 = machine.Pin(19)
        self.gp20 = machine.Pin(20)
        self.gp21 = machine.Pin(21)
        self.gp22 = machine.Pin(22)
        self.gp25 = machine.Pin(25)
        self.gp26 = machine.Pin(26)
        self.gp27 = machine.Pin(27)
        self.gp28 = machine.Pin(28)

        self.adc_channel_map = {
            '0': self.gp26,
            '1': self.gp27,
            '2': self.gp28,
            '4': 4  # Pin doesn't have ADC capabilities
        }

        self.pwm_channel_map = {
            "0A": [self.gp0, self.gp16],
            "0B": [self.gp1, self.gp17],
            "1A": [self.gp2, self.gp18],
            "1B": [self.gp3, self.gp19],
            "2A": [self.gp4, self.gp20],
            "2B": [self.gp5, self.gp21],
            "3A": [self.gp6, self.gp22],
            "3B": [self.gp7],
            "4A": [self.gp8],
            "4B": [self.gp9, self.gp25],
            "5A": [self.gp10, self.gp26],
            "5B": [self.gp11, self.gp27],
            "6A": [self.gp12, self.gp28],
            "6B": [self.gp13],
            "7A": [self.gp14],
            "7B": [self.gp15]
        }

        self.pin_usage_map = {}
        self._is_initialized = True

    @classmethod
    def pin_id(cls, pin: machine.Pin):
        m = re.search(r'\d+', str(pin))
        return int(m.group(0))

    def assert_free_pin(self, pin):
        self.assert_initialized()
        usage = self.pin_usage_map.get(self.pin_id(pin))
        if usage is not None:
            raise Exception("Pin {pin} is already in use as a {usage}".format(pin=str(pin), usage=usage))

    def assert_initialized(self):
        if not self._is_initialized:
            raise Exception("Pico singleton not initialized, constructor called directly")

    def reserve_pin(self, pin, usage='RAW'):
        self.pin_usage_map[self.pin_id(pin)] = usage
        return pin

    def signal(self, pin: machine.Pin, invert: bool = False, reservation: str = "Signal"):
        self.assert_free_pin(pin)
        self.reserve_pin(pin, reservation)
        return machine.Signal(pin, invert=invert)

    def adc(self, channel, reservation="ADC"):
        self.assert_initialized()
        if str(channel) not in (['0', '1', '2', '4']):
            raise ValueError("Channel {channel} is invalid".format(channel=channel))
        pin = self.adc_channel_map.get(str(channel))
        self.assert_free_pin(pin)
        self.reserve_pin(pin, reservation)
        return machine.ADC(pin)

    def pwm(self, channel, location='low', reservation="PWM"):
        self.assert_initialized()
        if self.pwm_channel_map.get(channel) is None:
            raise ValueError("Unknown PWM channel {}".format(channel))
        if location != 'low' and location != 'high':
            raise ValueError("Pin location must be 'low' or 'high' to specify e.g., channel 0A pin 0 versus 16")
        position = 0
        if location == 'high':
            position = 1

        pin = self.pwm_channel_map.get(channel)[position]
        if pin is None:
            raise Exception("No corresponding Pin for {channel} location {location}".format(channel=channel,location=location))
        self.assert_free_pin(pin)
        self.reserve_pin(pin, reservation)
        return machine.PWM(pin)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = Pico()
            cls._instance._initialize()
        return cls._instance

    def __str__(self):
        return str(self.pin_usage_map)
