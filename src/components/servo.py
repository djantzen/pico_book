class Servo:

    MID = 1520000
    MIN = 630000  # physical min is 500000
    MAX = 2440000  # physical max is 2470000
    FREQ = 60

    def __init__(self, pwm_pin, pwm_freq=FREQ):
        self.pwm = pwm_pin
        self.pwm.freq(pwm_freq)
        self.pwm

    def set_position(self, degrees=0):
        pulse = self.degrees_to_pulse(degrees)
        self.pwm.duty_ns(pulse)

    def degrees_to_pulse(self, degrees=0):
        if degrees < -90 or degrees > 90:
            raise ValueError("Degrees must be between -90 and 9")
        if degrees == 0:
            return Servo.MID
        if degrees < 0:
            return self._degrees_less_than_zero(degrees)
        if degrees > 0:
            return self._degrees_greater_than_zero(degrees)

    def _degrees_greater_than_zero(self, degrees):
        return int(Servo.MID - (degrees / 90 * (Servo.MID - Servo.MIN)))

    def _degrees_less_than_zero(self, degrees):
        return int((degrees / -90 * (Servo.MAX - Servo.MID)) + Servo.MID)
