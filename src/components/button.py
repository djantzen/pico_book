from machine import Pin
import singletons


class Button:

    def __init__(self):
        self.pico = singletons.Pico.instance()
        self.pico.gp10.init(Pin.IN, Pin.PULL_DOWN)

    def is_pressed(self):
        return self.pico.gp10.value() == 1
