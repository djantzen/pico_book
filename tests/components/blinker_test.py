import unittest
import components
import singletons


class BlinkerTest(unittest.TestCase):

    def test_something(self):
        pico = singletons.Pico.instance()
        b = components.Blinker(pico.gp19)
        self.assertIsNotNone(b)
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
