"""
Classes to assist with testing. PinEvent is a simple container of old and new values. StateTrackable is a
base class that records a series of state changes described as PinEvents. Pin, PWM and ADC are mocks that
extend StateTrackable.
"""


class PinEvent:
    def __init__(self, old_value, new_value):
        self.event_id = None
        self.old_value = old_value
        self.new_value = new_value

    def set_id(self, event_id):
        self.event_id = event_id

    def __str__(self):
        return "Event {} with old value {}, new value {}".format(self.event_id, self.old_value, self.new_value)


class StateTrackable:
    def __init__(self):
        self.events = []
        self.event_id = 1

    def record_event(self, event: PinEvent):
        event.set_id(self.event_id)
        self.events.append(event)
        self.event_id += 1

    def get_event(self, event_id: int) -> PinEvent:
        for e in self.events:
            if e.event_id == event_id:
                return e

    def __str__(self):
        return "{}".format(self.events)


class Pin(StateTrackable):

    OPEN_DRAIN = 2
    IRQ_FALLING = 4
    IRQ_RISING = 8
    IN = "in"
    OUT = "out"
    PULL_UP = 1
    PULL_DOWN = 2

    def __init__(self, id, dir="in"):
        super().__init__()
        self.id = id
        self.mock_value = None
        self.dir = dir
        self.pull = None
        self.irq_falling_handler = None
        self.irq_rising_handler = None

    def init(self, dir="in", pull=None):
        self.mock_value = None
        self.dir = dir
        self.pull = pull

    def value(self, value=None):
        if value is None:
            return self.mock_value
        event = PinEvent(self.mock_value, value)
        self.record_event(event)
        self.mock_value = event.new_value
        if self.irq_rising_handler is not None:
            if event.old_value is None or event.new_value > event.old_value:
                self.irq_rising_handler(self)
        if self.irq_falling_handler is not None:
            if event.new_value is not None and event.new_value < event.old_value:
                self.irq_falling_handler(self)

    def irq(self, handler, trigger: int = (IRQ_FALLING | IRQ_RISING | OPEN_DRAIN), priority: int = 1,
            wake: int = None, hard: bool = False):
        if trigger & self.IRQ_FALLING:
            self.irq_falling_handler = handler
        if trigger & self.IRQ_RISING:
            self.irq_rising_handler = handler

    def __str__(self):
        # Do not change the first 7 characters or it will break code to retrieve pin id
        return "Pin({}, mode=ALT, pull=PULL_DOWN, alt=31)".format(self.id)


class ADC(StateTrackable):
    def __init__(self, pin: Pin):
        super().__init__()
        self.pin = pin
        self.u16_value = None

    def write_u16(self, u16_value: int):
        event = PinEvent(old_value=self.u16_value, new_value=u16_value)
        self.record_event(event)
        self.u16_value = u16_value

    def read_u16(self) -> int:
        return self.u16_value


class PWM(StateTrackable):
    def __init__(self, pin: Pin):
        super().__init__()
        self.pin = pin
        self.duty_ns_value = None
        self.duty_u16_value = None
        self.freq_value = None

    def duty_ns(self, duty_ns_value=None):
        if duty_ns_value is None:
            return self.duty_ns_value
        else:
            event = PinEvent(old_value=self.duty_ns_value, new_value=duty_ns_value)
            self.record_event(event)
            self.duty_ns_value = duty_ns_value

    def duty_u16(self, duty_u16_value=None):
        if duty_u16_value is None:
            return self.duty_u16_value
        else:
            event = PinEvent(old_value=self.duty_u16_value, new_value=duty_u16_value)
            self.record_event(event)
            self.duty_u16_value = duty_u16_value

    def freq(self, freq_value):
        if freq_value is None:
            return self.freq_value
        else:
            self.freq_value = freq_value

