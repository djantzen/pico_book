import machine


class PirSensor:

    def __init__(self, pin):
        self.pin = pin
        self.pin.init(machine.Pin.IN, machine.Pin.PULL_DOWN)

    def on_movement(self, handler):
        self.pin.irq(trigger=machine.Pin.IRQ_RISING, handler=handler)
