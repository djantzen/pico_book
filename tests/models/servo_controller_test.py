import unittest
import singletons
import models
import components


def clear_pico():
    singletons.Pico._instance = None


class ServoControllerTest(unittest.TestCase):

    def test_voltage_to_degrees_mid_min_max(self):
        self.assertEqual(models.ServoController.voltage_to_degrees(32767.5), 0)
        self.assertEqual(models.ServoController.voltage_to_degrees(models.servo_controller.MIN_V - 1), -90)
        self.assertEqual(models.ServoController.voltage_to_degrees(models.servo_controller.MAX_V + 1), 90)

    def test_voltage_to_degrees_at_45(self):
        self.assertEqual(models.ServoController.voltage_to_degrees(16383.75), -45)
        self.assertEqual(models.ServoController.voltage_to_degrees(49151.25), 45)

    def test_adjust_sets_servo_writes_to_lcd(self):
        clear_pico()
        controller = models.ServoController()
        controller.knob.adc.write_u16(16383.75)
        controller.adjust()
        self.assertEqual(controller.servo.pwm.duty_ns(), 1980000)
        self.assertEqual(controller.lcd.rs_pin.get_event(8).new_value, components.LCD.CHARACTER_MODE)
