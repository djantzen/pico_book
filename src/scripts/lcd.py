
import utime
from singletons import Pico
from components import LCD, Servo

pico = Pico.instance()
lcd = LCD(rs_pin=pico.reserve_pin(pico.gp0, "LCD RS"),
          e_pin=pico.reserve_pin(pico.gp1, "LCD E"),
          d4_pin=pico.reserve_pin(pico.gp2, "LCD D4"),
          d5_pin=pico.reserve_pin(pico.gp3, "LCD D5"),
          d6_pin=pico.reserve_pin(pico.gp4, "LCD D6"),
          d7_pin=pico.reserve_pin(pico.gp5, "LCD D7"))
lcd.configure()
knob = pico.adc('0', reservation="Potentiometer ADC")
pwm_seven_b = pico.pwm('7B', reservation="Servo controller PWM")
servo = Servo(pwm_seven_b)
MAX_V = 65000
MIN_V = 13100

print(pico)

def voltage_to_degrees(voltage):
    if voltage > MAX_V:
        return 90
    if voltage < MIN_V:
        return -90
    percentage = voltage / 65535
    return int((percentage * 180) - 90)

# Define main program code
def main():

    while True:
        lcd.write("Knob turned to ", LCD.LINE_1)
        voltage = knob.read_u16()
        print(str(voltage))
        degrees = voltage_to_degrees(voltage)
        print(str(degrees))
        lcd.write(str(degrees), LCD.LINE_2)
        servo.set_position(degrees)
        utime.sleep(3)


# End of main program code


try:
    main()

except KeyboardInterrupt:
    pass

finally:
    print("finally")
    lcd.send_bits(0x01, LCD.COMMAND_MODE)
    lcd.write("So long!", LCD.LINE_1)
    lcd.write("MBTechWorks.com", LCD.LINE_2)
