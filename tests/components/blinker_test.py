import unittest
import components


class BlinkerTest(unittest.TestCase):

    def test_something(self):
        b = components.Blinker()
        self.assertIsNotNone(b)
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
