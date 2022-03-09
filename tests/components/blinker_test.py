import unittest
import components
import singletons


class BlinkerTest(unittest.TestCase):

    def test_blink_once(self):
        pico = singletons.Pico.instance()
        b = components.Blinker(pico.gp25, 0)
#        pico.gp25.expect().to_receive("blink").and_return()
        b.blink()

        self.assertEqual(pico.gp25.events[0].old_value, None)
        self.assertEqual(pico.gp25.events[0].new_value, b'1')
        self.assertEqual(pico.gp25.events[1].old_value, b'1')
        self.assertEqual(pico.gp25.events[1].new_value, b'0')
        self.assertEqual(True, True)  # add assertion here
