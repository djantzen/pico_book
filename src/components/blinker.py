import utime
import machine
import singletons


class Blinker:
    def __init__(self, timeout=2):
        self.timeout = timeout
        self.pico = singletons.Pico.instance()
        self.pico.gp19.init(machine.Pin.OUT)

    def blink(self):
        self.pico.gp19.value(1)
        utime.sleep(self.timeout)
        self.pico.gp19.value(0)
        utime.sleep(self.timeout)

