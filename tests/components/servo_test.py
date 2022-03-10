import unittest
import components
import singletons


def clear_pico():
    singletons.Pico._instance = None


class ServoTest(unittest.TestCase):

    def test_degrees_to_pulse(self):
        self.assertEqual(components.servo.degrees_to_pulse(-90), components.servo.MAX)
        self.assertEqual(components.servo.degrees_to_pulse(-45), 1980000)
        self.assertEqual(components.servo.degrees_to_pulse(0), components.servo.MID)
        self.assertEqual(components.servo.degrees_to_pulse(45), 1075000)
        self.assertEqual(components.servo.degrees_to_pulse(90), components.servo.MIN)
