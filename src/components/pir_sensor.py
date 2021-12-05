import machine


class PirSensor:

    def __init__(self, pin):
        self.handler = None
        self.pin = pin
        self.pin.init(machine.Pin.IN, machine.Pin.PULL_DOWN)

    def movement(self):
        return self.pin.value() == 1

    def _pin_handler(self, pin):
        self.handler()

    def handle_interrupt(self, handler):
        self.handler = handler
        self.pin.irq(trigger=machine.Pin.IRQ_RISING, handler=self._pin_handler)
