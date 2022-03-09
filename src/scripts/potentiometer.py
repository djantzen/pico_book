import utime
import components
import singletons

pico = singletons.Pico.instance()
potentiometer = components.Potentiometer(pico.adc("0", "Potentiometer ADC"))
led = pico.pwm("7B", "LED PWM")
led.freq(1000)


def converter(reading):
    return reading * 3.3 / 65535


for i in range(50000):
    print(potentiometer.read_u16(converter))
    led.duty_u16(potentiometer.read_u16())

led.duty_u16(0)
