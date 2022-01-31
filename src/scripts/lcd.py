# MBTechWorks.com 2016
# Control an LCD 1602 display from Raspberry Pi with Python programming

# !/usr/bin/python

# Pinout of the LCD:
# 1 : GND
# 2 : 5V power
# 3 : Display contrast - Connect to middle pin potentiometer
# 4 : RS (Register Select)
# 5 : R/W (Read Write) - Ground this pin (important)
# 6 : Enable or Strobe
# 7 : Data Bit 0 - data pin 0, 1, 2, 3 are not used
# 8 : Data Bit 1 -
# 9 : Data Bit 2 -
# 10: Data Bit 3 -
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V
# 16: LCD Backlight GND

import time
import machine
import singletons
from singletons import Pico

pico = singletons.Pico.instance()

# GPIO to LCD mapping
# LCD_RS = 7  # Pi pin 26
# LCD_E = 8  # Pi pin 24
# LCD_D4 = 25  # Pi pin 22
# LCD_D5 = 24  # Pi pin 18
# LCD_D6 = 23  # Pi pin 16
# LCD_D7 = 18  # Pi pin 12
LCD_RS = pico.gp0  # Pi pin 1
LCD_E = pico.gp1  # Pi pin 2
LCD_D4 = pico.gp2  # Pi pin 4
LCD_D5 = pico.gp3  # Pi pin 5
LCD_D6 = pico.gp4  # Pi pin 6
LCD_D7 = pico.gp5  # Pi pin 7

LCD_RS.init(machine.Pin.OUT)
LCD_E.init(machine.Pin.OUT)
LCD_D4.init(machine.Pin.OUT)
LCD_D5.init(machine.Pin.OUT)
LCD_D6.init(machine.Pin.OUT)
LCD_D7.init(machine.Pin.OUT)


# Device constants
# LCD_CHR = True  # Character mode
# LCD_CMD = False  # Command mode
LCD_CHR = 1  # Character mode
LCD_CMD = 0  # Command mode
LCD_CHARS = 16  # Characters per line (16 max)
LCD_LINE_1 = 0x80  # LCD memory location for 1st line
LCD_LINE_2 = 0xC0  # LCD memory location 2nd line


# Define main program code
def main():

    # Initialize display
    lcd_init()

    # Loop - send text and sleep 3 seconds between texts
    # Change text to anything you wish, but must be 16 characters or less

    while True:
        lcd_text("Hello World!", LCD_LINE_1)
        lcd_text("", LCD_LINE_2)

        lcd_text("Raspberry Pi", LCD_LINE_1)
        lcd_text("16x2 LCD Display", LCD_LINE_2)

        time.sleep(3)  # 3 second delay

        lcd_text("ABCDEFGHIJKLMNOP", LCD_LINE_1)
        lcd_text("1234567890123456", LCD_LINE_2)

        time.sleep(3)  # 3 second delay

        lcd_text("I love my", LCD_LINE_1)
        lcd_text("Raspberry Pi!", LCD_LINE_2)

        time.sleep(3)

        lcd_text("MBTechWorks.com", LCD_LINE_1)
        lcd_text("For more R Pi", LCD_LINE_2)

        time.sleep(3)


# End of main program code


# Initialize and clear display
def lcd_init():
    lcd_write(0x33, LCD_CMD)  # Initialize
    lcd_write(0x32, LCD_CMD)  # Set to 4-bit mode
    lcd_write(0x06, LCD_CMD)  # Cursor move direction
    lcd_write(0x0C, LCD_CMD)  # Turn cursor off
    lcd_write(0x28, LCD_CMD)  # 2 line display
    lcd_write(0x01, LCD_CMD)  # Clear display
    time.sleep(0.0005)  # Delay to allow commands to process


def lcd_write(bits, mode):
    # High bits
#   GPIO.output(LCD_RS, mode)  # RS
    LCD_RS.value(mode)

    LCD_D4.value(0)
    LCD_D5.value(0)
    LCD_D6.value(0)
    LCD_D7.value(0)
    if bits & 0x10 == 0x10:
        LCD_D4.value(1)
    if bits & 0x20 == 0x20:
        LCD_D5.value(1)
    if bits & 0x40 == 0x40:
        LCD_D6.value(1)
    if bits & 0x80 == 0x80:
        LCD_D7.value(1)

    # Toggle 'Enable' pin
    lcd_toggle_enable()

    # Low bits
    LCD_D4.value(0)
    LCD_D5.value(0)
    LCD_D6.value(0)
    LCD_D7.value(0)
    if bits & 0x01 == 0x01:
        LCD_D4.value(1)
    if bits & 0x02 == 0x02:
        LCD_D5.value(1)
    if bits & 0x04 == 0x04:
        LCD_D6.value(1)
    if bits & 0x08 == 0x08:
        LCD_D7.value(1)

    # Toggle 'Enable' pin
    lcd_toggle_enable()


def lcd_toggle_enable():
    time.sleep(0.0005)
    LCD_E.value(1)
    time.sleep(0.0005)
    LCD_E.value(0)
    time.sleep(0.0005)


def lcd_text(message, line):
    # Send text to display
#    message = message.ljust(LCD_CHARS, " ")
    print(message)
    lcd_write(line, LCD_CMD)

    # print(message)
    # print("Length is ", len(message))
    for i in range(LCD_CHARS):
        if i < len(message):
            # print("I is ", i)
            # print("Char is ", message[i])
            lcd_write(ord(message[i]), LCD_CHR)
        else:
            lcd_write(ord(" "), LCD_CHR)



# Begin program
try:
    main()

except KeyboardInterrupt:
    pass

finally:
    print("finally")
    lcd_write(0x01, LCD_CMD)
    lcd_text("So long!", LCD_LINE_1)
    lcd_text("MBTechWorks.com", LCD_LINE_2)
