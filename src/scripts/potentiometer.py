import utime
import components
import singletons

pico = singletons.Pico.instance()
potentiometer = components.Potentiometer(pico.gp26_adc0)


def converter(reading):
    return reading * 3.3 / 65535


while True:
    print(potentiometer.read_u16(converter))
    utime.sleep(2)

