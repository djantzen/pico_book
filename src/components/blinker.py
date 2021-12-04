import _thread

import utime
import machine


class Blinker:
    def __init__(self, pin, timeout=2, delay=2):
        self.timeout = timeout
        self.delay = delay
        self.pin = pin
        self.pin.init(machine.Pin.OUT)

    def on(self):
        self.pin.value(1)

    def off(self):
        self.pin.value(0)

    def blink(self):
        self.on()
        utime.sleep(self.timeout)
        self.off()
        utime.sleep(self.delay)

