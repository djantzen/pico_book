from machine import Pin


class Button:

    def __init__(self, pin):
        self.pin = pin
        self.pin.init(Pin.IN, Pin.PULL_DOWN)

    def is_pressed(self):
        return self.pin.value() == 1
