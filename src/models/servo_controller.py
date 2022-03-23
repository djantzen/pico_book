from singletons import Pico
from components import Potentiometer, LCD, Servo

MAX_V = 65000
MIN_V = 13100


class ServoController:

    def __init__(self):
        pico = Pico.instance()
        self.lcd = LCD(rs_pin=pico.reserve_pin(pico.gp0, "LCD RS"),
                       e_pin=pico.reserve_pin(pico.gp1, "LCD E"),
                       d4_pin=pico.reserve_pin(pico.gp2, "LCD D4"),
                       d5_pin=pico.reserve_pin(pico.gp3, "LCD D5"),
                       d6_pin=pico.reserve_pin(pico.gp4, "LCD D6"),
                       d7_pin=pico.reserve_pin(pico.gp5, "LCD D7"))
        self.lcd.configure()
        self.knob = Potentiometer(pico.adc('0', reservation="Potentiometer ADC"))
        self.servo = Servo(pico.pwm('7B', reservation="Servo controller PWM"))

    @classmethod
    def voltage_to_degrees(cls, voltage):
        if voltage > MAX_V:
            return 90
        if voltage < MIN_V:
            return -90
        percentage = voltage / 65535
        return int((percentage * 180) - 90)

    def adjust(self):
        voltage = self.knob.read_u16()
        degrees = ServoController.voltage_to_degrees(voltage)
        self.lcd.write("Knob turned to ", LCD.LINE_1)
        self.lcd.write(str(degrees), LCD.LINE_2)
        self.servo.set_position(degrees)
