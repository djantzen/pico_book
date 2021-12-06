#

class ADC:
    def __init__(self, pin):
        ...

class PinEvent:
    def __init__(self, old_value, new_value):
        self.old_value = old_value
        self.new_value = new_value

class Pin:
    IN = "in"
    OUT = "out"

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

    def value(self, value):
        print("mocking value ", value)
        if value is None:
            return 1 if self.mock_value == b"1" else 0
        event = PinEvent(self.mock_value, (b"1" if value else b"0"))
        self.events.append(event)
        self.mock_value = event.new_value
