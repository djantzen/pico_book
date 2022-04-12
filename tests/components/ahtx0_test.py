import unittest

from components import AHTX0
from singletons import Pico, ClockTower
from components.ahtx0 import I2C_ADDRESS


class AHTX0Test(unittest.TestCase):

    def setup(self) -> None:
        Pico._instance = None
        ClockTower.instance().set_sleep_duration(0)
        pico = Pico.instance()
        i2c = pico.i2c(sda=pico.gp16, scl=pico.gp17, reservation="AHTXO")
        i2c.generator.add(addr=I2C_ADDRESS, message=b'\x00\x00\x00\x00\x00\x005')  # uncalibrated
        i2c.generator.add(I2C_ADDRESS, b'\x18\x00\x00\x00\x00\x005')  # calibrated, not busy
        self.sensor = AHTX0(i2c=i2c)

    def teardown(self) -> None:
        Pico._instance = None
        ClockTower.instance().set_sleep_duration(0)

    def test_reset(self) -> None:
        self.setup()

        self.sensor.reset()
        result = self.sensor.i2c.get_message(I2C_ADDRESS, 3).payload
        self.assertEqual(result[0], 0xBA)

        self.teardown()

    def test_calibrate(self) -> None:
        self.setup()

        self.sensor.calibrate()
        result = self.sensor.i2c.get_message(I2C_ADDRESS, 3).payload
        self.assertEqual(0xE1, result[0])
        self.assertEqual(0x08, result[1])
        self.assertEqual(0x00, result[2])
        self.teardown()

    def test_measure_and_read(self) -> None:
        self.setup()

        self.sensor.i2c.generator.add(I2C_ADDRESS, b'\x1c:S\xe5\xcdu\xe7')

        self.sensor.measure()
        result = self.sensor.i2c.get_message(I2C_ADDRESS, 3).payload  # after calibration, send measurement command
        self.assertEqual(0xAC, result[0])
        self.assertEqual(0x33, result[1])
        self.assertEqual(0x00, result[2])
        measurements = self.sensor.read()  # must not throw an exception
        self.assertAlmostEqual(22.78423309326172, measurements['humidity'])  # checking exact equality fails, float weirdness?
        self.assertAlmostEqual(22.53208160400391, measurements['temperature'])
        self.teardown()

    def test_read_throws_exception_before_measure(self) -> None:
        self.setup()
        self.assertRaises(Exception, self.sensor.read)
        self.teardown()
