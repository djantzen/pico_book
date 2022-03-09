import machine

MID: int = 1520000
MIN: int = 630000  # physical min is 500000
MAX: int = 2440000  # physical max is 2470000
FREQ: int = 60


def _degrees_greater_than_zero(degrees):
    return int(MID - (degrees / 90 * (MID - MIN)))


def _degrees_less_than_zero(degrees):
    return int((degrees / -90 * (MAX - MID)) + MID)


def degrees_to_pulse(degrees=0):
    if degrees < -90 or degrees > 90:
        raise ValueError("Degrees must be between -90 and 9")
    if degrees == 0:
        return MID
    if degrees < 0:
        return _degrees_less_than_zero(degrees)
    if degrees > 0:
        return _degrees_greater_than_zero(degrees)


class Servo:

    def __init__(self, pwm_pin: machine.PWM, pwm_freq: int = FREQ):
        self.pwm = pwm_pin
        self.pwm.freq(pwm_freq)

    def set_position(self, degrees: int = 0):
        pulse = degrees_to_pulse(degrees)
        self.pwm.duty_ns(pulse)
