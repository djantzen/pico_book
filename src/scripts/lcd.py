
import utime
from singletons import Pico
from components import LCD

pico = Pico.instance()
lcd = LCD(rs_pin=pico.gp0, e_pin=pico.gp1, d4_pin=pico.gp2,
          d5_pin=pico.gp3, d6_pin=pico.gp4, d7_pin=pico.gp5)


# Define main program code
def main():

    while True:
        lcd.write("Hello World!", LCD.LINE_1)
        lcd.write("", LCD.LINE_2)

        lcd.write("Raspberry Pi", LCD.LINE_1)
        lcd.write("16x2 LCD Display", LCD.LINE_2)

        utime.sleep(3)  # 3 second delay

        lcd.write("So Cool, so cool", LCD.LINE_1)
        lcd.write("1234567890123456", LCD.LINE_2)

        utime.sleep(3)  # 3 second delay

        lcd.write("I love my", LCD.LINE_1)
        lcd.write("Raspberry Pi!", LCD.LINE_2)

        utime.sleep(3)

        lcd.write("MBTechWorks.com", LCD.LINE_1)
        lcd.write("For more R Pi", LCD.LINE_2)

        utime.sleep(3)


# End of main program code

try:
    main()

except KeyboardInterrupt:
    pass

finally:
    print("finally")
    lcd.send_bits(0x01, LCD.CMD)
    lcd.write("So long!", LCD.LINE_1)
    lcd.write("MBTechWorks.com", LCD.LINE_2)
