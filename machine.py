class Pin:
    IN = "in"
    OUT = "out"
    PULL_UP = 1
    PULL_DOWN = 2

    def __init__(self, id, dir="in"):
        self.id = id
        self.mock_value = None
        self.dir = dir
        self.pull = None
        self.events = []

    def init(self, dir="in", pull=None):
        self.mock_value = None
        self.dir = dir
        self.pull = pull

    def value(self, value=None):
        print("mocking value ", value)
        if value is None:
            return 1 if self.mock_value == b"1" else 0
        event = PinEvent(self.mock_value, (b"1" if value else b"0"))
        self.events.append(event)
        self.mock_value = event.new_value

    def __str__(self):
        return "Pin({}, mode=ALT, pull=PULL_DOWN, alt=31)".format(self.id)


class ADC:
    def __init__(self, pin: Pin):
        self.pin = pin

    def read_u16(self):
        ...


class PWM:
    def __init__(self, pin: Pin):
        self.pin = pin

    def duty_ns(self, ns):
        ...

    def freq(self, freq):
        ...


class PinEvent:
    def __init__(self, old_value, new_value):
        self.old_value = old_value
        self.new_value = new_value
