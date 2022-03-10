import machine


class Dimmer:

    def __init__(self, pwm: machine.PWM):
        self.pwm = pwm
        self.pwm.freq(1000)

    def freq(self, freq: int):
        self.pwm.freq(freq)

    def duty_u16(self, duty_u16_value):
        self.duty_u16(duty_u16_value)

    def off(self):
        self.duty_u16(0)
