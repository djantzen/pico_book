import components.esp32
import singletons
from components.esp32 import requests

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in $ROOT/secrets.py, please add them there!")
    raise

singletons.Pico._instance = None
pico = singletons.Pico.instance()
cs_pin = pico.reserve_pin(pico.gp9, "CS")
reset_pin = pico.reserve_pin(pico.gp12, "Reset")
gpio0_pin = pico.reserve_pin(pico.gp6, "GPIO 0")
sck_pin = pico.gp10
mosi_pin = pico.gp11
miso_pin = pico.gp8

ready_pin = pico.reserve_pin(pico.gp7)

spi = pico.spi(id=1, sck=sck_pin, mosi=mosi_pin, miso=miso_pin)

esp = components.esp32.Control(spi=spi, gpio0_pin=gpio0_pin, ready_pin=ready_pin, reset_pin=reset_pin, cs_pin=cs_pin, debug=3)
requests.set_interface(esp)
wifi = components.esp32.WiFiManager(esp=esp, secrets=secrets, status_pixel=None)


print("Connected to", str(esp.ssid, 'utf-8'), "\tRSSI:", esp.rssi)
print("My IP address is", esp.pretty_ip(esp.ip_address))
print("IP lookup adafruit.com: %s" % esp.pretty_ip(esp.get_host_by_name("adafruit.com")))
print("Ping google.com: %d ms" % esp.ping("google.com"))

r = wifi.get('https://www.google.com')

print(r.content)
