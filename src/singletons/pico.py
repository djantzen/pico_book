import machine


class Pico:
    _instance = None

    gp0 = machine.Pin(0)
    gp1 = machine.Pin(1)
    gp2 = machine.Pin(2)
    gp3 = machine.Pin(3)
    gp4 = machine.Pin(4)
    gp5 = machine.Pin(5)
    gp6 = machine.Pin(6)
    gp7 = machine.Pin(7)
    gp8 = machine.Pin(8)
    gp9 = machine.Pin(9)
    gp10 = machine.Pin(10)
    gp11 = machine.Pin(11)
    gp12 = machine.Pin(12)
    gp13 = machine.Pin(13)
    gp14 = machine.Pin(14)
    gp15 = machine.Pin(15)
    gp16 = machine.Pin(16)
    gp17 = machine.Pin(17)
    gp18 = machine.Pin(18)
    gp19 = machine.Pin(19)
    gp20 = machine.Pin(20)
    gp21 = machine.Pin(21)
    gp22 = machine.Pin(22)
    gp25 = machine.Pin(25)
    gp26 = machine.Pin(26)
    gp27 = machine.Pin(27)
    gp28 = machine.Pin(28)
    # Note if a pin is used directly it cannot also be used when wrapped in an ADC/PWM
    adc_0_gp26 = machine.ADC(gp26)
    adc_1_gp27 = machine.ADC(gp27)
    adc_2_gp28 = machine.ADC(gp28)
    adc_4_onboard = machine.ADC(4)
    pwm_0a_gp0 = machine.PWM(gp0)
    pwm_0b_gp1 = machine.PWM(gp1)
    pwm_1a_gp2 = machine.PWM(gp2)
    pwm_1b_gp3 = machine.PWM(gp3)
    pwm_2a_gp4 = machine.PWM(gp4)
    pwm_2b_gp5 = machine.PWM(gp5)
    pwm_3a_gp6 = machine.PWM(gp6)
    pwm_3b_gp7 = machine.PWM(gp7)
    pwm_4a_gp8 = machine.PWM(gp8)
    pwm_4b_pg9 = machine.PWM(gp9)
    pwm_5a_gp10 = machine.PWM(gp10)
    pwm_5b_gp11 = machine.PWM(gp11)
    pwm_6a_gp12 = machine.PWM(gp12)
    pwm_6b_gp13 = machine.PWM(gp13)
    pwm_7a_gp14 = machine.PWM(gp14)
    pwm_7b_gp15 = machine.PWM(gp15)
    pwm_0a_gp16 = machine.PWM(gp16)
    pwm_0b_gp17 = machine.PWM(gp17)
    pwm_1a_gp18 = machine.PWM(gp18)
    pwm_1b_gp19 = machine.PWM(gp19)
    pwm_2a_gp20 = machine.PWM(gp20)
    pwm_2b_gp21 = machine.PWM(gp21)
    pwm_3a_gp22 = machine.PWM(gp22)
    pwm_5a_gp26 = machine.PWM(gp26)
    pwm_5b_gp27 = machine.PWM(gp27)
    pwm_6a_gp28 = machine.PWM(gp28)

    def __init__(self):
        ...

    @classmethod
    def instance(klass):
        if klass._instance is None:
            klass._instance = Pico()
        return klass._instance

    def to_s(self) -> str:
        """echo"""

