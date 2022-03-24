import unittest
import components
import singletons


class BlinkerTest(unittest.TestCase):

    def setup(self):
        singletons.Pico._instance = None
        singletons.ClockTower.instance().set_sleep_duration(0)

    def teardown(self):
        singletons.Pico._instance = None
        singletons.ClockTower.instance().set_sleep_duration(None)

    def test_blink_once(self):
        self.setup()
        pico = singletons.Pico.instance()
        pin = pico.gp25
        b = components.Blinker(pico.reserve_pin(pin, "Blinker"))
        b.blink()
        self.assertEqual(pico.gp25.get_event(1).old_value, None)
        self.assertEqual(pico.gp25.get_event(1).new_value, 1)
        self.assertEqual(pico.gp25.get_event(2).old_value, 1)
        self.assertEqual(pico.gp25.get_event(2).new_value, 0)
        self.teardown()
