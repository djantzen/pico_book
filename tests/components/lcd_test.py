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

    def test_initialization(self):
        self.before()
        for i in range(1, 7):
            self.assertEqual(self.lcd.rs_pin.get_event(i).new_value, components.LCD.COMMAND_MODE)

        # 0x33
        self.assertEqual(self.lcd.d5_pin.get_event(2).new_value, 1)
        self.assertEqual(self.lcd.d4_pin.get_event(2).new_value, 1)
        self.assertEqual(self.lcd.d5_pin.get_event(4).new_value, 1)
        self.assertEqual(self.lcd.d4_pin.get_event(4).new_value, 1)

        # 0x32
        self.assertEqual(self.lcd.d5_pin.get_event(6).new_value, 1)
        self.assertEqual(self.lcd.d4_pin.get_event(6).new_value, 1)
        self.assertEqual(self.lcd.d5_pin.get_event(8).new_value, 1)

        # for i in range(15):
        #     print("---------------")
        #     print(self.lcd.d7_pin.get_event(i))

        # 0x06
        self.assertEqual(self.lcd.d5_pin.get_event(11).new_value, 1)
        self.assertEqual(self.lcd.d6_pin.get_event(7).new_value, 1)

        # 0x0c
        self.assertEqual(self.lcd.d6_pin.get_event(10).new_value, 1)
        self.assertEqual(self.lcd.d7_pin.get_event(9).new_value, 1)


    def test_line_one_message(self):
        self.before()
#        self.lcd.write("Tests are good.", components.LCD.LINE_1)
        self.lcd.write("T", components.LCD.LINE_1)
        # 84, 101, 115, 116, 115, 32, 97, 32, 103, 48, 48, 100, 46
        # print(ord("T"))
        # for i in range(25):
        #     print(self.lcd.rs_pin.get_event(i))
        self.assertEqual(self.lcd.rs_pin.get_event(8).new_value, components.LCD.CHARACTER_MODE)
        self.assertEqual(self.lcd.d6_pin.get_event(18).new_value, 1)  # high bits
        self.assertEqual(self.lcd.d4_pin.get_event(20).new_value, 1)
        self.assertEqual(self.lcd.d6_pin.get_event(19).new_value, 0)  # low bits
        self.assertEqual(self.lcd.d6_pin.get_event(20).new_value, 1)
        # 128 64 32 16    8 4 2 1

        # 84 high 4, 1. low 4 -- x40 x10 x04, pins d6, d4, e_pin 1, e_pin 0, d6