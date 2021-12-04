import unittest
import components
import singletons


class ButtonTest(unittest.TestCase):

    def test_press_once(self):
        ...
        # pico = singletons.Pico.instance()
        # b = components.Button(pico.gp19, 0)
        # b.blink()
        #
        # self.assertEqual(pico.gp19.events[0].old_value, None)
        # self.assertEqual(pico.gp19.events[0].new_value, b'1')
        # self.assertEqual(pico.gp19.events[1].old_value, b'1')
        # self.assertEqual(pico.gp19.events[1].new_value, b'0')
        # self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
