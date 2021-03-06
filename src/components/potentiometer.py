class Potentiometer:

    def __init__(self, adc):
        self.adc = adc

    def read_u16(self, converter=None) -> float:
        if converter:
            return converter(self.adc.read_u16())
        else:
            return self.adc.read_u16()
