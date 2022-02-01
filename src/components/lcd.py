import machine
import utime

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

# https://www.mbtechworks.com/projects/drive-an-lcd-16x2-display-with-raspberry-pi.html


class LCD:

    CHR = 1  # Character mode
    CMD = 0  # Command mode
    CHARS = 16  # Characters per line (16 max)
    LINE_1 = 0x80  # LCD memory location for 1st line
    LINE_2 = 0xC0  # LCD memory location 2nd line

    def __init__(self, rs_pin, e_pin, d4_pin, d5_pin, d6_pin, d7_pin):
        self.rs_pin = rs_pin
        self.e_pin = e_pin
        self.d4_pin = d4_pin
        self.d5_pin = d5_pin
        self.d6_pin = d6_pin
        self.d7_pin = d7_pin

        self.rs_pin.init(machine.Pin.OUT)
        self.e_pin.init(machine.Pin.OUT)
        self.d4_pin.init(machine.Pin.OUT)
        self.d5_pin.init(machine.Pin.OUT)
        self.d6_pin.init(machine.Pin.OUT)
        self.d7_pin.init(machine.Pin.OUT)

        self.send_bits(0x33, LCD.CMD)  # Initialize
        self.send_bits(0x32, LCD.CMD)  # Set to 4-bit mode
        self.send_bits(0x06, LCD.CMD)  # Cursor move direction
        self.send_bits(0x0C, LCD.CMD)  # Turn cursor off
        self.send_bits(0x28, LCD.CMD)  # 2 line display
        self.send_bits(0x01, LCD.CMD)  # Clear display
        utime.sleep(0.0005)  # Delay to allow commands to process

    def send_bits(self, bits, mode):
        # High bits
        self.rs_pin.value(mode)

        self.d4_pin.value(0)
        self.d5_pin.value(0)
        self.d6_pin.value(0)
        self.d7_pin.value(0)
        if bits & 0x10 == 0x10:
            self.d4_pin.value(1)
        if bits & 0x20 == 0x20:
            self.d5_pin.value(1)
        if bits & 0x40 == 0x40:
            self.d6_pin.value(1)
        if bits & 0x80 == 0x80:
            self.d7_pin.value(1)

        # Toggle 'Enable' pin
        self.lcd_toggle_enable()

        # Low bits
        self.d4_pin.value(0)
        self.d5_pin.value(0)
        self.d6_pin.value(0)
        self.d7_pin.value(0)
        if bits & 0x01 == 0x01:
            self.d4_pin.value(1)
        if bits & 0x02 == 0x02:
            self.d5_pin.value(1)
        if bits & 0x04 == 0x04:
            self.d6_pin.value(1)
        if bits & 0x08 == 0x08:
            self.d7_pin.value(1)

        # Toggle 'Enable' pin
        self.lcd_toggle_enable()

    def write(self, message, line):
        self.send_bits(line, LCD.CMD)

        for i in range(LCD.CHARS):
            if i < len(message):
                self.send_bits(ord(message[i]), LCD.CHR)
            else:
                self.send_bits(ord(" "), LCD.CHR)

    def lcd_toggle_enable(self):
        utime.sleep(0.0005)
        self.e_pin.value(1)
        utime.sleep(0.0005)
        self.e_pin.value(0)
        utime.sleep(0.0005)
