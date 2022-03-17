import unittest
import components
import singletons


def clear_pico():
    singletons.Pico._instance = None


class BlinkerTest(unittest.TestCase):

    def test_blink_once(self):
        clear_pico()
        pico = singletons.Pico.instance()
        singletons.ClockTower.instance().set_sleep_duration(0)
        pin = pico.gp25
        b = components.Blinker(pico.reserve_pin(pin, "Blinker"))
        b.blink()
        self.assertEqual(pico.gp25.get_event(1).old_value, None)
        self.assertEqual(pico.gp25.get_event(1).new_value, 1)
        self.assertEqual(pico.gp25.get_event(2).old_value, 1)
        self.assertEqual(pico.gp25.get_event(2).new_value, 0)
