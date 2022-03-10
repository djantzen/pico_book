import components
import singletons

pico = singletons.Pico.instance()
potentiometer = components.Potentiometer(pico.adc("0", "Potentiometer ADC"))
pwm = pico.pwm("7B", "LED PWM")
dimmer = components.Dimmer(pwm)


def converter(reading):
    return reading * 3.3 / 65535


for i in range(50000):
    print(potentiometer.read_u16(converter))
    dimmer.duty_u16(potentiometer.read_u16())

dimmer.off()
