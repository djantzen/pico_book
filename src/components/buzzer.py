from machine import Pin
import utime


class Buzzer:

    def __init__(self, pin, timeout=1):
        self.pin = pin
        self.pin.init(Pin.OUT)
        self.timeout = timeout

    def buzz(self):
        for i in range(10):
            self._oscillate(50)
            utime.sleep(0.5)

    def _oscillate(self, duration):
        for i in range(duration):
            self.pin.value(1)
            utime.sleep_ms(3)
            self.pin.value(0)
