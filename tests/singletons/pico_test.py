import unittest
import singletons


class PicoTest(unittest.TestCase):

    def test_something(self):
        p = singletons.Pico.instance()

        self.assertIsNotNone(p)
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
