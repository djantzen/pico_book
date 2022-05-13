"""

Library for the AHT10/20 Humidity and Temperature sensor.

Based on:
  https://github.com/adafruit/Adafruit_CircuitPython_AHTx0/blob/main/adafruit_ahtx0.py
  https://github.com/Chouffy/python_sensor_aht20/blob/main/AHT20.py
  https://cdn-learn.adafruit.com/assets/assets/000/091/676/original/AHT20-datasheet-2020-4-16.pdf
  https://www.avrfreaks.net/forum/aht20-sensor-and-i2c
"""
from micropython import const
from machine import I2C
from singletons import ClockTower

I2C_ADDRESS: int = const(0x38)
IS_BUSY: int = const(0x80)
IS_CALIBRATED: int = const(0x08)
RESET_COMMAND = bytearray([0xBA])
CALIBRATE_COMMAND = bytes([0xE1, 0x08, 0x00])
MEASURE_COMMAND = bytes([0xAC, 0x33, 0x00])


class AHTX0:

    """Construct a new sensor, it will soft reset and calibrate if necessary"""
    def __init__(self, i2c: I2C):
        self.i2c = i2c
        self._measurement = bytearray(6)

    def reset(self) -> None:
        self.i2c.writeto(I2C_ADDRESS, RESET_COMMAND)
        ClockTower.instance().sleep(0.04)

    def check_status(self, status) -> bool:
        try:
            return self.i2c.readfrom(I2C_ADDRESS, 1)[0] & status == status
        except OSError as e:
            print("Caught {}".format(e))
            return False

    def calibrate(self, force: bool = False) -> None:
        if not self.check_status(IS_CALIBRATED) or force:
            self.i2c.writeto(I2C_ADDRESS, CALIBRATE_COMMAND)

    """Take a measurement. This must be called prior to 'read()'"""
    def measure(self) -> None:
        try:
            self.i2c.writeto(I2C_ADDRESS, MEASURE_COMMAND)
        except OSError as e:
            print("OSError {}".format(e))
        while self.check_status(IS_BUSY):
            ClockTower.instance().sleep(0.1)
        self._measurement = self.i2c.readfrom(I2C_ADDRESS, 7)

    """Read the last measurement taken. Exception will be thrown if no measurement has been taken"""
    def read(self) -> dict:
        if self._measurement[0] == 0x00:
            raise Exception("Call for a measurement first")
        temperature = self._transform_temperature()
        humidity = self._transform_humidity()
        return {'temperature': temperature, 'humidity': humidity}

    # Transformation: https://cdn-learn.adafruit.com/assets/assets/000/091/676/original/AHT20-datasheet-2020-4-16.pdf
    def _transform_humidity(self) -> float:
        return (self._bitshift_humidity() / pow(2, 20)) * 100

    # Transformation: https://cdn-learn.adafruit.com/assets/assets/000/091/676/original/AHT20-datasheet-2020-4-16.pdf
    def _transform_temperature(self) -> float:
        return (self._bitshift_temperature() / pow(2, 20)) * 200 - 50

    # Discussion here: https://www.avrfreaks.net/forum/aht20-sensor-and-i2c
    # The data returned from the device contains 2.5 bytes for humidity and 2.5 for temperature. To reconstruct
    # the original value recorded by the device and transmitted, the bits must be shifted into their original places
    # to reflect the proper integer value prior to transformation
    def _bitshift_humidity(self) -> int:
        # shift first byte 1.5 bytes left, next byte .5 bytes, take least significant 4 bits of the last
        return (self._measurement[1] << 12) | (self._measurement[2] << 4) | (self._measurement[3] >> 4)

    def _bitshift_temperature(self) -> int:
        # shift the lower 4 bits 2 bytes left, next byte by 1 byte, append last byte
        return ((self._measurement[3] & 0xF) << 16) | (self._measurement[4] << 8) | self._measurement[5]
