import unittest
import components
import singletons


def clear_pico():
    singletons.Pico._instance = None


class LCDTest(unittest.TestCase):

    def before(self):
        clear_pico()
        pico = singletons.Pico.instance()
        self.lcd = components.LCD(rs_pin=pico.reserve_pin(pico.gp0, "LCD RS"),
                                  e_pin=pico.reserve_pin(pico.gp1, "LCD E"),
                                  d4_pin=pico.reserve_pin(pico.gp2, "LCD D4"),
                                  d5_pin=pico.reserve_pin(pico.gp3, "LCD D5"),
                                  d6_pin=pico.reserve_pin(pico.gp4, "LCD D6"),
                                  d7_pin=pico.reserve_pin(pico.gp5, "LCD D7"))

    def test_setup(self):
        self.before()
        self.lcd.configure()
        for i in range(1, 7):
            self.assertEqual(self.lcd.rs_pin.get_event(i).new_value, components.LCD.COMMAND_MODE)

    def test_initialize(self):
        self.before()
        self.lcd.initialize()
        self.assertEqual(self.lcd.d5_pin.get_event(1).new_value, 1)
        self.assertEqual(self.lcd.d4_pin.get_event(1).new_value, 1)
        self.assertEqual(self.lcd.d5_pin.get_event(3).new_value, 1)
        self.assertEqual(self.lcd.d4_pin.get_event(3).new_value, 1)

    def test_set_four_bit_mode(self):
        self.before()
        self.lcd.set_four_bit_mode()
        self.assertEqual(self.lcd.d5_pin.get_event(1).new_value, 1)
        self.assertEqual(self.lcd.d4_pin.get_event(1).new_value, 1)
        self.assertEqual(self.lcd.d5_pin.get_event(2).new_value, 0)
        self.assertEqual(self.lcd.d5_pin.get_event(3).new_value, 1)

    def test_set_cursor_move_direction(self):
        self.before()
        self.lcd.set_cursor_move_direction()
        self.assertEqual(self.lcd.d5_pin.get_event(1).new_value, 1)
        self.assertEqual(self.lcd.d6_pin.get_event(1).new_value, 1)

    def test_turn_cursor_off(self):
        self.before()
        self.lcd.set_cursor_off()
        self.assertEqual(self.lcd.d6_pin.get_event(1).new_value, 1)
        self.assertEqual(self.lcd.d7_pin.get_event(1).new_value, 1)

    def test_two_line_display(self):
        self.before()
        self.lcd.set_two_line_display()
        self.assertEqual(self.lcd.d5_pin.get_event(1).new_value, 1)
        self.assertEqual(self.lcd.d7_pin.get_event(1).new_value, 1)

    def test_clear_display(self):
        self.before()
        self.lcd.clear_display()
        self.assertEqual(self.lcd.d4_pin.get_event(1).new_value, 1)

    def test_line_one_message(self):
        self.before()
        self.lcd.configure()
        self.lcd.write("Tests are good.", components.LCD.LINE_1)

        self.assertEqual(self.lcd.rs_pin.get_event(7).new_value, components.LCD.COMMAND_MODE)
        self.assertEqual(self.lcd.rs_pin.get_event(8).new_value, components.LCD.CHARACTER_MODE)
        self.assertEqual(self.lcd.d6_pin.get_event(1).new_value, 1)
        self.assertEqual(self.lcd.d4_pin.get_event(1).new_value, 1)

    def test_line_two_message(self):
        self.before()
        self.lcd.configure()
        self.lcd.write("Tests are good.", components.LCD.LINE_2)

        self.assertEqual(self.lcd.rs_pin.get_event(7).new_value, components.LCD.COMMAND_MODE)
        self.assertEqual(self.lcd.rs_pin.get_event(8).new_value, components.LCD.CHARACTER_MODE)
        self.assertEqual(self.lcd.d7_pin.get_event(1).new_value, 1)
        self.assertEqual(self.lcd.d6_pin.get_event(1).new_value, 1)

        d4_high_char = '0'  # 48 (d5 and d4)
        d5_high_char = ' '  # 32 (d5)
        d6_high_char = '@'  # 64 (d6)
        d7_high_char = 'Ç'  # 128 (d7)
        d4_low_char = '3'   # 51 (d5h, d4h, d5l, d4l)
        d5_low_char = '*'   # 42 (d5h, d7l, d5l)
        d6_low_char = '8'   # 56 (d5h, d4h, d7l)
        d7_low_char = '$'   # 36 (d5h, d6l)

    def test_d5_and_d4_high_pins_4_bit(self):
        self.before()
        d4_high_char = '0'  # decimal 48 (d5 and d4)
        self.lcd.write(d4_high_char, components.LCD.LINE_1)
        self.assertEqual(self.lcd.d5_pin.get_event(1).new_value, 1)
        self.assertEqual(self.lcd.d4_pin.get_event(1).new_value, 1)

    def test_d6_high_pin_4_bit(self):
        self.before()
        d6_high_char = '@'  # 64 (d6)
        self.lcd.write(d6_high_char, components.LCD.LINE_1)
        self.assertEqual(self.lcd.d6_pin.get_event(1).new_value, 1)

    def test_d6_low_pin_4_bit(self):
        self.before()
        d6_low_char = '$'  # 36 (d5h, d6l)
        self.lcd.write(d6_low_char, components.LCD.LINE_1)
        self.assertEqual(self.lcd.d6_pin.get_event(1).new_value, 1)

    def test_d7_high_pin_4_bit(self):
        self.before()
        d7_high_char = 'Ç'  # 128 (d7)
        self.lcd.write(d7_high_char, components.LCD.LINE_1)
        self.assertEqual(self.lcd.d7_pin.get_event(1).new_value, 1)

    def test_d7_low_pin_4_bit(self):
        self.before()
        d7_low_char = '('
        self.lcd.write(d7_low_char, components.LCD.LINE_1)
        self.assertEqual(self.lcd.d7_pin.get_event(1).new_value, 1)

    def test_d4_d5_low_pins_4_bit(self):
        self.before()
        d7_low_char = '3'  # 51 (d5h, d4h, d5l, d4l)
        self.lcd.write(d7_low_char, components.LCD.LINE_1)
        self.assertEqual(self.lcd.d5_pin.get_event(3).new_value, 1)
        self.assertEqual(self.lcd.d4_pin.get_event(3).new_value, 1)
