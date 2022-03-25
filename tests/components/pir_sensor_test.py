from components import PirSensor
from singletons import Pico
import unittest


class PirSensorTest(unittest.TestCase):

    def setup(self):
        Pico._instance = None

    def teardown(self):
        Pico._instance = None

    def test_irq_rising(self):
        self.setup()

        pir = PirSensor(Pico.instance().gp28)
        flag = False

        def handler(pin):
            nonlocal flag
            flag = True

        pir.on_movement(handler)
        self.assertFalse(flag)
        pir.pin.value(1)
        self.assertTrue(flag)
        self.teardown()
