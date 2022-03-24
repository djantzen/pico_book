import unittest

import utime

import singletons
import models
import components


def wait_until(obj, variable, state, limit=10, sleep=0.1):
    for i in range(limit):
        value = getattr(obj, variable)
        if value == state:
            return
        else:
            utime.sleep(sleep)


class TrafficLightTest(unittest.TestCase):

    def setup(self):
        singletons.Pico._instance = None
        singletons.ClockTower.instance().set_sleep_duration(0)
        self.light = models.TrafficLight()
        self.light.start()

    def teardown(self):
        self.light.stop()
        singletons.Pico._instance = None
        singletons.ClockTower.instance().set_sleep_duration(None)

    def test_traffic_light_normal_cycle(self):
        self.setup()

        self.light.cycle()
        self.assertEqual(self.light.green_light.pin.get_event(1).new_value, 1)
        self.assertEqual(self.light.green_light.pin.get_event(2).new_value, 0)
        self.assertEqual(self.light.yellow_light.pin.get_event(1).new_value, 1)
        self.assertEqual(self.light.yellow_light.pin.get_event(2).new_value, 0)
        self.assertEqual(self.light.red_light.pin.get_event(1).new_value, 1)
        self.assertEqual(self.light.red_light.pin.get_event(2).new_value, 0)

        self.teardown()

    def test_walk_button_interrupts_cycle(self):
        self.setup()

        self.light.button.pin.value(1)
        # the button watcher thread needs time to set the flag in the main thread
        wait_until(self.light, "button_pressed", True)
        self.light.cycle()

        self.assertEqual(self.light.red_light.pin.get_event(1).new_value, 1)
        self.assertEqual(self.light.red_light.pin.get_event(2).new_value, 0)
        self.assertEqual(self.light.buzzer.pin.get_event(1).new_value, 1)
        self.assertEqual(self.light.buzzer.pin.get_event(2).new_value, 0)

        self.assertEqual(self.light.green_light.pin.get_event(1).new_value, 1)
        self.assertEqual(self.light.green_light.pin.get_event(2).new_value, 0)
        self.assertEqual(self.light.yellow_light.pin.get_event(1).new_value, 1)
        self.assertEqual(self.light.yellow_light.pin.get_event(2).new_value, 0)
        self.assertEqual(self.light.red_light.pin.get_event(3).new_value, 1)
        self.assertEqual(self.light.red_light.pin.get_event(4).new_value, 0)

        self.teardown()
