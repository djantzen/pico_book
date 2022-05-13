from singletons import Pico, ClockTower
from components import AHTX0, LCD
from components.esp32 import Control, requests, WiFiManager
import uasyncio

class EnvMonitor:

    def __init__(self, secrets):

        pico = Pico.instance()
        cs_pin = pico.reserve_pin(pico.gp9, "ESP CS")
        reset_pin = pico.reserve_pin(pico.gp12, "ESP Reset")
        gpio0_pin = pico.reserve_pin(pico.gp6, "ESP GPIO 0")
        ready_pin = pico.reserve_pin(pico.gp7, "ESP Ready")
        self.relay_pin = pico.reserve_pin(pico.gp27, "Relay Switch")
        self.relay_pin.init(mode=1)

        spi = pico.spi(id=1, sck=pico.gp10, mosi=pico.gp11, miso=pico.gp8, reservation="ESP SPI")
        esp = Control(spi=spi, gpio0_pin=gpio0_pin, ready_pin=ready_pin, reset_pin=reset_pin, cs_pin=cs_pin, debug=0)
        requests.set_interface(esp)
        self.wifi = WiFiManager(esp=esp, secrets=secrets, status_pixel=None)

        i2c = pico.i2c(sda=pico.gp16, scl=pico.gp17, reservation="AHTXO")
        self.ahtx0 = AHTX0(i2c=i2c)

        self.lcd = LCD(rs_pin=pico.reserve_pin(pico.gp0, "LCD RS"),
                       e_pin=pico.reserve_pin(pico.gp1, "LCD E"),
                       d4_pin=pico.reserve_pin(pico.gp2, "LCD D4"),
                       d5_pin=pico.reserve_pin(pico.gp3, "LCD D5"),
                       d6_pin=pico.reserve_pin(pico.gp4, "LCD D6"),
                       d7_pin=pico.reserve_pin(pico.gp5, "LCD D7"))

        self.telemetry_url = "http://{}:8080/api/v1/{}/telemetry".format(secrets['thingsboard_host'], secrets['device_token'])
        self.rpc_url = "http://{}:8080/api/v1/{}/rpc".format(secrets['thingsboard_host'], secrets['device_token'])

    def initialize(self):
        self.lcd.configure()
        self.ahtx0.reset()
        self.ahtx0.calibrate()

    def take_reading(self):
        self.ahtx0.measure()
        reading = self.ahtx0.read()
        self.lcd.write("Temp {}".format(reading["temperature"]), LCD.LINE_1)
        self.lcd.write("Humidity {}".format(reading["humidity"]), LCD.LINE_2)
        reading['valve_is_open'] = self.relay_pin.value()
        reading['ts'] = ClockTower.instance().now

        return reading

    def record(self, reading):
        try:
            self.wifi.post(self.telemetry_url, json=reading)
        except RuntimeError as re:
            print("Caught {}".format(re))
            self.wifi.reset()

    def get_command(self, timeout_ms=60000):
        try:
            print("getting rpc from {}".format(self.rpc_url))
            resp = self.wifi.get(self.rpc_url + "?timeout={}".format(timeout_ms))
            print("returned from rpc")
            payload = resp.json()
            print("payload {}".format(payload))
            if "method" in payload:
                if payload["method"] == "setZoneControllerStatus":
                    if 'params' in payload:
                        valve_command = payload['params']
                        self.relay_pin.value(valve_command)
                if payload["method"] == "getZoneControllerStatus":
                    self.wifi.post(self.rpc_url + "/{}".format(payload["id"]), json={"valve_is_open": self.relay_pin.value()})

        except RuntimeError as re:
            print("Caught {}".format(re))
            self.wifi.reset()

