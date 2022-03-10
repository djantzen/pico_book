import unittest
import components
import singletons


def clear_pico():
    singletons.Pico._instance = None


class ButtonTest(unittest.TestCase):

    def test_is_pressed(self):
        clear_pico()
        pico = singletons.Pico.instance()
        b = components.Button(pico.reserve_pin(pico.gp19, "Button"))
        self.assertFalse(b.is_pressed())
        pico.gp19.value(1)
        self.assertTrue(b.is_pressed())
