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

# Based on:
#   https://www.mbtechworks.com/projects/drive-an-lcd-16x2-display-with-raspberry-pi.html


class LCD:

    CHARACTER_MODE = 1  # Character mode
    COMMAND_MODE = 0  # Command mode
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

        self.high_bit_map = {
            128: self.d7_pin,
            64: self.d6_pin,
            32: self.d5_pin,
            16: self.d4_pin,
        }
        self.low_bit_map = {
            8: self.d7_pin,
            4: self.d6_pin,
            2: self.d5_pin,
            1: self.d4_pin
        }

    def configure(self):
        self.initialize()
        self.set_four_bit_mode()
        self.set_cursor_off()
        self.set_cursor_move_direction()
        self.set_two_line_display()
        self.clear_display()
        utime.sleep(0.0005)  # Delay allows commands to process

    def initialize(self):
        # Command is decimal 51
        self.send_bits(0x33, LCD.COMMAND_MODE)

    def set_four_bit_mode(self):
        # Command is decimal 50
        self.send_bits(0x32, LCD.COMMAND_MODE)

    def set_cursor_move_direction(self):
        # Command is decimal 6
        self.send_bits(0x06, LCD.COMMAND_MODE)

    def set_cursor_off(self):
        # Command is decimal 12
        self.send_bits(0x0C, LCD.COMMAND_MODE)

    def set_two_line_display(self):
        # Command is decimal 40
        self.send_bits(0x28, LCD.COMMAND_MODE)

    def clear_display(self):
        self.send_bits(0x01, LCD.COMMAND_MODE)

    def _select_pins(self, bits, pin_map):
        for key in pin_map.keys():
            pin = pin_map.get(key & bits)
            if pin is not None:
                pin.value(1)

    def send_bits(self, bits, mode):

        # High bits
        self.rs_pin.value(mode)
        self._clear_pins()
        self._select_pins(bits, self.high_bit_map)

        # Toggle 'Enable' pin
        self.lcd_toggle_enable()

        # Low bits
        self._clear_pins()
        self._select_pins(bits, self.low_bit_map)

        # Toggle 'Enable' pin
        self.lcd_toggle_enable()

    def _clear_pins(self):
        if self.d4_pin.value() is not None and self.d4_pin.value() > 0:
            self.d4_pin.value(0)
        if self.d5_pin.value() is not None and self.d5_pin.value() > 0:
            self.d5_pin.value(0)
        if self.d6_pin.value() is not None and self.d6_pin.value() > 0:
            self.d6_pin.value(0)
        if self.d7_pin.value() is not None and self.d7_pin.value() > 0:
            self.d7_pin.value(0)

    def write(self, message, line):
        self.send_bits(line, LCD.COMMAND_MODE)

        for i in range(LCD.CHARS):
            if i < len(message):
                self.send_bits(ord(message[i]), LCD.CHARACTER_MODE)
            else:
                self.send_bits(ord(" "), LCD.CHARACTER_MODE)

    def lcd_toggle_enable(self):
        utime.sleep(0.0005)
        self.e_pin.value(1)
        utime.sleep(0.0005)
        self.e_pin.value(0)
        utime.sleep(0.0005)
