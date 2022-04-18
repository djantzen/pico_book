import unittest
import _thread
from components.esp32 import Control
from singletons import Pico, ClockTower


class ControlTest(unittest.TestCase):

    def toggle_ready_pin(self):
        # CS PIN = 0 and READY PIN == 1 and vice versa
        while self.test_running:
            self.ready_pin.value((self.cs_pin.value() - 1) * -1)
            ClockTower.instance().sleep(0.05)
        return

    def setup(self):
        self.test_running = True
        Pico._instance = None
        pico = Pico.instance()

        self.cs_pin = pico.reserve_pin(pico.gp9, "CS")
        self.reset_pin = pico.reserve_pin(pico.gp11, "Reset")
        self.gpio0_pin = pico.reserve_pin(pico.gp10, "GPIO 0")
        self.ready_pin = pico.reserve_pin(pico.gp12, "Ready/Is Busy")
        sck_pin = pico.gp6
        miso_pin = pico.gp8
        mosi_pin = pico.gp7

        self.spi = pico.spi(sck=sck_pin, mosi=mosi_pin, miso=miso_pin)
        self.esp = Control(spi=self.spi, gpio0_pin=self.gpio0_pin, ready_pin=self.ready_pin, reset_pin=self.reset_pin,
                           cs_pin=self.cs_pin, debug=3)

        _thread.start_new_thread(self.toggle_ready_pin, ())

    def teardown(self):
        self.test_running = False
        Pico._instance = None

    def test_ping(self):
        self.setup()
        self.spi.generator.add(bytes([0xE0]))  # START name lookup
        self.spi.generator.add(bytes([0x34 | 1 << 7]))
        self.spi.generator.add(bytes([1]))
        self.spi.generator.add(bytes([1]))
        self.spi.generator.add(bytes([0x01]))
        self.spi.generator.add(bytes([0xEE]))  # END

        self.spi.generator.add(bytes([0xE0]))  # START
        self.spi.generator.add(bytes([0xB5]))
        self.spi.generator.add(bytes([0x1]))
        self.spi.generator.add(bytes([0x4]))
        self.spi.generator.add(bytes([0x8E, 0xFA, 0xD9, 0x6E]))
        self.spi.generator.add(bytes([0xEE]))  # END

        self.spi.generator.add(bytes([0xE0]))  # START
        self.spi.generator.add(bytes([0xBE]))
        self.spi.generator.add(bytes([0x1]))
        self.spi.generator.add(bytes([0x2]))
        self.spi.generator.add(bytes([0x1E, 0x0]))  # response of 30 ms
        self.spi.generator.add(bytes([0xEE]))  # END
        res = self.esp.ping("github.com")

        self.assertEqual(30, res)
        self.assertEqual(bytes([0xe0, 0x34, 0x1, 0xa, 0x67, 0x69, 0x74, 0x68, 0x75, 0x62, 0x2e, 0x63, 0x6f, 0x6d, 0xee, 0x0]), self.spi.get_message(1).payload[0:16])
        self.assertEqual(bytes([0xe0, 0x35, 0x0, 0xee]), self.spi.get_message(2).payload[0:4])
        self.assertEqual(bytes([0xe0, 0x3e, 0x2, 0x4, 0x8e, 0xfa, 0xd9, 0x6e, 0x1, 0xfa, 0xee, 0x63]), self.spi.get_message(3).payload[0:12])
        self.teardown()



