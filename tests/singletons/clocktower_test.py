import unittest
import singletons


class ClockTowerTest(unittest.TestCase):

    def test_something(self):
        c = singletons.ClockTower.instance()

        self.assertIsNotNone(c)
        print("Now ", c.now())
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
