import utime
import components
import singletons

pico = singletons.Pico.instance()
potentiometer = components.Potentiometer(pico.adc_0_gp26)
led = pico.pwm_7b_gp15
led.freq(1000)


def converter(reading):
    return reading * 3.3 / 65535


while True:
    print(potentiometer.read_u16(converter))
    led.duty_u16(potentiometer.read_u16())

