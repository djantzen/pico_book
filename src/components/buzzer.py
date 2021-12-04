from machine import Pin
import utime


class Buzzer:

    def __init__(self, pin, timeout=1):
        self.pin = pin
        self.pin.init(Pin.OUT)
        self.timeout = timeout

    def buzz(self):
        for i in range(10):
            self.pin.value(1)
            utime.sleep(1)
            self.pin.value(0)
            utime.sleep(0.5)
