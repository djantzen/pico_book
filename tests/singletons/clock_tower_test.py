import unittest
import singletons
import utime


class ClockTowerTest(unittest.TestCase):

    def test_fetch_instance(self):
        c = singletons.ClockTower.instance()
        self.assertIsNotNone(c)

    def test_set_time(self):
        c = singletons.ClockTower.instance()
        now = utime.time() - 60
        c.set_now(now)
        self.assertEqual(c.now(), now)
