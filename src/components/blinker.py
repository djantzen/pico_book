import utime
import machine


class Blinker:
    def __init__(self, pin, timeout=2):
        self.timeout = timeout
        self.pin = pin
        self.pin.init(machine.Pin.OUT)

    def blink(self):
        self.pin.value(1)
        utime.sleep(self.timeout)
        self.pin.value(0)
        utime.sleep(self.timeout)

