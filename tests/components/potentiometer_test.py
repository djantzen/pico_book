import unittest
import components
import singletons


def clear_pico():
    singletons.Pico._instance = None


class PotentiometerTest(unittest.TestCase):

    def test_read_u16(self):
        clear_pico()
        pico = singletons.Pico.instance()
        adc = pico.adc("0", "Potentiometer ADC")
        potentiometer = components.Potentiometer(adc)
        adc.write_u16(5.0)
        self.assertEqual(potentiometer.read_u16(), 5.0)


