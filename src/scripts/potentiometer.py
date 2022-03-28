import components
import singletons

runtime = int(input("Run for how many seconds?"))
pico = singletons.Pico.instance()
potentiometer = components.Potentiometer(pico.adc("0", "Potentiometer ADC"))
pwm = pico.pwm("7B", "LED PWM")
dimmer = components.Dimmer(pwm)


def converter(reading):
    return reading * 3.3 / 65535


while singletons.ClockTower.instance().not_yet(runtime):
    print(potentiometer.read_u16(converter))
    dimmer.duty_u16(potentiometer.read_u16())

dimmer.off()
