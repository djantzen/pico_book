import unittest
from singletons import Pico, ClockTower
from models import EnvMonitor
import components


class EnvMonitorTest(unittest.TestCase):

    def setup(self):
        Pico._instance = None
        secrets = { "ssid": "the_network", "password": "the_password",
                    "thingsboard_host": "some.host.com",
                    "device_token": "token" }
        self.monitor = EnvMonitor(secrets=secrets)
        self.monitor.ahtx0.i2c.generator.add(addr=components.ahtx0.I2C_ADDRESS, message=b'\x18\x00\x00\x00\x00\x005')  # calibrated, not busy

    def teardown(self):
        Pico._instance = None

    def test_initialization(self):
        self.setup()

        self.assertIsNotNone(self.monitor)
        self.monitor.initialize()

        self.teardown()
