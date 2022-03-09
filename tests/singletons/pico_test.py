import unittest

import machine
import singletons


class PicoTest(unittest.TestCase):

    @classmethod
    def clearPico(cls):
        singletons.Pico._instance = None

    def test_fetch_instance(self):
        self.clearPico()
        p = singletons.Pico.instance()
        self.assertIsNotNone(p)

    def test_adc(self):
        self.clearPico()
        p = singletons.Pico.instance()
        adc_zero = p.adc("0")
        adc_one = p.adc("1")
        adc_two = p.adc("2")
        adc_four = p.adc("4")

        try:
            p.adc("3")
        except ValueError:
            pass

        self.assertIsInstance(adc_zero, machine.ADC)
        self.assertIsInstance(adc_one, machine.ADC)
        self.assertIsInstance(adc_two, machine.ADC)
        self.assertIsInstance(adc_four, machine.ADC)

    def test_pwm(self):
        self.clearPico()
        p = singletons.Pico.instance()
        try:
            p.pwm("A0")
        except ValueError:
            pass

        self.assertEqual(0, singletons.Pico.pin_id(p.pwm("0A", "low").pin))
        self.assertEqual(1, singletons.Pico.pin_id(p.pwm("0B", "low").pin))
        self.assertEqual(2, singletons.Pico.pin_id(p.pwm("1A", "low").pin))
        self.assertEqual(3, singletons.Pico.pin_id(p.pwm("1B", "low").pin))
        self.assertEqual(4, singletons.Pico.pin_id(p.pwm("2A", "low").pin))
        self.assertEqual(5, singletons.Pico.pin_id(p.pwm("2B", "low").pin))
        self.assertEqual(6, singletons.Pico.pin_id(p.pwm("3A", "low").pin))
        self.assertEqual(7, singletons.Pico.pin_id(p.pwm("3B", "low").pin))
        self.assertEqual(8, singletons.Pico.pin_id(p.pwm("4A", "low").pin))
        self.assertEqual(9, singletons.Pico.pin_id(p.pwm("4B", "low").pin))
        self.assertEqual(10, singletons.Pico.pin_id(p.pwm("5A", "low").pin))
        self.assertEqual(11, singletons.Pico.pin_id(p.pwm("5B", "low").pin))
        self.assertEqual(12, singletons.Pico.pin_id(p.pwm("6A", "low").pin))
        self.assertEqual(13, singletons.Pico.pin_id(p.pwm("6B", "low").pin))
        self.assertEqual(14, singletons.Pico.pin_id(p.pwm("7A", "low").pin))
        self.assertEqual(15, singletons.Pico.pin_id(p.pwm("7B", "low").pin))
        self.assertEqual(16, singletons.Pico.pin_id(p.pwm("0A", "high").pin))
        self.assertEqual(17, singletons.Pico.pin_id(p.pwm("0B", "high").pin))
        self.assertEqual(18, singletons.Pico.pin_id(p.pwm("1A", "high").pin))
        self.assertEqual(19, singletons.Pico.pin_id(p.pwm("1B", "high").pin))
        self.assertEqual(20, singletons.Pico.pin_id(p.pwm("2A", "high").pin))
        self.assertEqual(21, singletons.Pico.pin_id(p.pwm("2B", "high").pin))
        self.assertEqual(22, singletons.Pico.pin_id(p.pwm("3A", "high").pin))
        self.assertEqual(26, singletons.Pico.pin_id(p.pwm("5A", "high").pin))
        self.assertEqual(27, singletons.Pico.pin_id(p.pwm("5B", "high").pin))
        self.assertEqual(28, singletons.Pico.pin_id(p.pwm("6A", "high").pin))
